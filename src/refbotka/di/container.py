from __future__ import annotations

from typing import AsyncIterable

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from botka.db.session import create_engine, create_sessionmaker
from botka.services.refinance_client import RefinanceClient
from botka.services.user_service import UserService
from refbotka.config import Settings


class AppProvider(Provider):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._settings = settings

    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return self._settings

    @provide(scope=Scope.APP)
    def engine(self, settings: Settings) -> AsyncEngine:
        return create_engine(settings.database_url)

    @provide(scope=Scope.APP)
    def sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker:
        return create_sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    async def session(
        self, sessionmaker: async_sessionmaker
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def user_service(self, session: AsyncSession, settings: Settings) -> UserService:
        return UserService(session, settings)  # type: ignore[arg-type]

    @provide(scope=Scope.APP)
    async def refinance_client(
        self, settings: Settings
    ) -> AsyncIterable[RefinanceClient]:
        client = RefinanceClient(settings)  # type: ignore[arg-type]
        if client.is_configured:
            await client.verify_bot_entity()
        yield client


def build_container(settings: Settings) -> AsyncContainer:
    return make_async_container(AppProvider(settings))
