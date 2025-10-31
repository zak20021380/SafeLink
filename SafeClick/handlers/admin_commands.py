"""Administrative command handlers."""
from __future__ import annotations

import asyncio
import logging
from typing import List

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from bot.database import Database
from bot.strings import get_string
from bot.utils import chunked

LOGGER = logging.getLogger(__name__)


def _database(context: ContextTypes.DEFAULT_TYPE) -> Database:
    return context.application.bot_data["database"]


def _config(context: ContextTypes.DEFAULT_TYPE):
    return context.application.bot_data["config"]


def _is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    return (
        update.effective_user is not None
        and update.effective_user.id in _config(context).admin_ids
    )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update, context):
        if update.effective_chat:
            language = "en"
            await update.effective_chat.send_message(
                get_string("admin_only", language)
            )
        return
    stats = await _database(context).get_global_stats()
    await update.effective_chat.send_message(
        get_string(
            "admin_panel",
            "en",
            user_count=stats["user_count"],
            total_scans=stats["total_scans"],
        ),
        parse_mode=ParseMode.MARKDOWN,
    )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update, context):
        if update.effective_chat:
            await update.effective_chat.send_message(get_string("admin_only", "en"))
        return
    if not context.args:
        await update.effective_chat.send_message(get_string("broadcast_prompt", "en"))
        return
    message = " ".join(context.args)
    user_ids = await _database(context).get_all_user_ids()
    await update.effective_chat.send_message(
        get_string("broadcast_confirm", "en", count=len(user_ids))
    )
    success = 0
    for batch in chunked(user_ids, 30):
        tasks = []
        for user_id in batch:
            tasks.append(_send_broadcast(context, user_id, message))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        success += sum(1 for result in results if result is True)
        await asyncio.sleep(0.5)
    await update.effective_chat.send_message(
        get_string("broadcast_done", "en") + f" ({success}/{len(user_ids)})"
    )


async def _send_broadcast(
    context: ContextTypes.DEFAULT_TYPE, user_id: int, message: str
) -> bool:
    try:
        await context.bot.send_message(user_id, message)
        return True
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.debug("Broadcast to %s failed: %s", user_id, exc)
        return False


async def force_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update, context):
        if update.effective_chat:
            await update.effective_chat.send_message(get_string("admin_only", "en"))
        return
    if len(context.args) < 2:
        await update.effective_chat.send_message(
            get_string("invalid_arguments", "en")
        )
        return
    try:
        channel_id = int(context.args[0])
    except ValueError:
        await update.effective_chat.send_message(
            get_string("invalid_arguments", "en")
        )
        return
    channel_username = context.args[1]
    await _database(context).set_force_join(
        enabled=True, channel_id=channel_id, channel_username=channel_username
    )
    await update.effective_chat.send_message(
        get_string("force_join_enabled", "en", channel=channel_username)
    )


async def disable_force_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update, context):
        if update.effective_chat:
            await update.effective_chat.send_message(get_string("admin_only", "en"))
        return
    await _database(context).set_force_join(enabled=False)
    await update.effective_chat.send_message(get_string("force_join_disabled", "en"))


def build_admin_handlers() -> List:
    return [
        CommandHandler("admin", admin_panel),
        CommandHandler("broadcast", broadcast),
        CommandHandler("forcejoin", force_join),
        CommandHandler("disableforcejoin", disable_force_join),
    ]
