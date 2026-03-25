from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name=__name__)

HELP_TEXT = (
    "Available commands:\n"
    "\n"
    "/help — show this message.\n"
    "\n"
    "Finance:\n"
    "/transfer [@username | reply] &lt;amount&gt; &lt;currency&gt; [comment] — send money (creates a draft, you confirm).\n"
    "/request [@username | reply] &lt;amount&gt; &lt;currency&gt; [comment] — request money from someone (they confirm or deny).\n"
    "/balance [@username] — show balance and recent activity.\n"
    "/deposit &lt;amount&gt; &lt;currency&gt; — top up your balance via Keepz.\n"
    "/transactions — show your last 10 transactions.\n"
    "/split &lt;amount&gt; &lt;currency&gt; @recipient [comment] — create a split campaign.\n"
    "/split_join [id] [amount] — join a split (reply to card or provide id).\n"
    "/split_add [id] @user [amount] — add someone to a split.\n"
    "/split_leave [id] [@user] — leave a split (or creator removes @user).\n"
    "/splits — list your open splits."
)


@router.message(Command("help", "start"))
async def help_handler(message: Message) -> None:
    await message.answer(HELP_TEXT)
