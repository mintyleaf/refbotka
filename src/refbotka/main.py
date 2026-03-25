from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from botka.db.session import init_models
from botka.handlers import refinance
from botka.middlewares import UserSyncMiddleware
from dishka.integrations.aiogram import setup_dishka
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from refbotka.config import Settings
from refbotka.di.container import build_container
from refbotka.handlers.help import router as help_router


async def _run() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()

    container = build_container(settings)
    engine = await container.get(AsyncEngine)
    await init_models(engine)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(help_router)
    dp.include_router(refinance.commands.router)
    dp.include_router(refinance.callbacks.router)

    setup_dishka(container, dp)

    sessionmaker = await container.get(async_sessionmaker)
    user_sync = UserSyncMiddleware(sessionmaker, settings)  # type: ignore[arg-type]
    dp.message.middleware(user_sync)
    dp.callback_query.middleware(user_sync)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await container.close()
        await bot.session.close()
        await engine.dispose()


def main() -> None:
    asyncio.run(_run())
