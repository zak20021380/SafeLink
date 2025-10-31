"""User command handlers for SafeClick."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from bot.database import Database
from bot.strings import get_string
from bot.utils import PhishTankClient, extract_urls, validate_url
from .callbacks import render_settings_view

LOGGER = logging.getLogger(__name__)


async def _get_language(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> str:
    prefs = await _database(context).get_user_preferences(user_id)
    return prefs.get("language", "en")


def _database(context: ContextTypes.DEFAULT_TYPE) -> Database:
    return context.application.bot_data["database"]


def _config(context: ContextTypes.DEFAULT_TYPE):
    return context.application.bot_data["config"]


def _phishtank(context: ContextTypes.DEFAULT_TYPE) -> PhishTankClient:
    return context.application.bot_data["phishtank"]


def _is_admin(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    return user_id in context.application.bot_data["config"].admin_ids


async def _check_force_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Ensure the user has joined the required channel if enabled."""
    if not update.effective_user:
        return False
    user_id = update.effective_user.id
    if _is_admin(user_id, context):
        return True

    settings = await _database(context).get_admin_settings()
    if not settings["force_join_enabled"]:
        return True

    channel_id = settings["force_join_channel_id"]
    channel_username = settings["force_join_channel_username"]
    if not channel_id:
        return True

    try:
        member = await context.bot.get_chat_member(channel_id, user_id)
        if member.status in {"left", "kicked"}:
            await update.effective_chat.send_message(
                get_string(
                    "force_join_required",
                    await _get_language(context, user_id),
                    channel=channel_username or channel_id,
                )
            )
            return False
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.exception("Force join check failed: %s", exc)
        return True
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return
    if not await _check_force_join(update, context):
        return
    user = update.effective_user
    await _database(context).upsert_user(user.id, user.username)
    stats = await _database(context).get_user_stats(user.id)
    language = await _get_language(context, user.id)

    stats_text = get_string(
        "start_stats",
        language,
        total_scans=stats.total_scans if stats else 0,
        phishing_found=stats.phishing_found if stats else 0,
        safe_found=stats.safe_found if stats else 0,
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("English", callback_data="lang_en"),
                InlineKeyboardButton("فارسی", callback_data="lang_fa"),
            ]
        ]
    )
    await update.effective_chat.send_message(
        f"{get_string('start_welcome', language)}\n\n{stats_text}\n\n{get_string('choose_language', language)}",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return
    if not await _check_force_join(update, context):
        return
    language = await _get_language(context, update.effective_user.id)
    await update.effective_chat.send_message(
        get_string("help", language), parse_mode=ParseMode.MARKDOWN
    )


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return
    if not await _check_force_join(update, context):
        return
    user_id = update.effective_user.id
    language = await _get_language(context, user_id)
    chat = update.effective_chat
    if not chat:
        return
    if not context.args:
        await chat.send_message(get_string("no_url_found", language))
        return
    url = context.args[0]
    if not url.startswith("http"):
        url = "http://" + url
    if not validate_url(url):
        await chat.send_message(get_string("no_url_found", language))
        return
    await _handle_scan(update, context, [url], language)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return
    if not await _check_force_join(update, context):
        return
    user_id = update.effective_user.id
    language = await _get_language(context, user_id)
    user_stats = await _database(context).get_user_stats(user_id)
    if not user_stats:
        await update.effective_chat.send_message(get_string("history_empty", language))
        return
    await update.effective_chat.send_message(
        get_string(
            "stats_message",
            language,
            total_scans=user_stats.total_scans,
            phishing_found=user_stats.phishing_found,
            safe_found=user_stats.safe_found,
            first_seen=user_stats.first_seen.strftime("%Y-%m-%d %H:%M"),
            last_active=user_stats.last_active.strftime("%Y-%m-%d %H:%M"),
        ),
        parse_mode=ParseMode.MARKDOWN,
    )


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return
    if not await _check_force_join(update, context):
        return
    user_id = update.effective_user.id
    language = await _get_language(context, user_id)
    records = await _database(context).get_recent_history(user_id)
    if not records:
        await update.effective_chat.send_message(get_string("history_empty", language))
        return
    lines = [get_string("history_header", language)]
    for record in records:
        lines.append(
            get_string(
                "history_item",
                language,
                scanned_at=record.scanned_at.strftime("%Y-%m-%d %H:%M"),
                url=record.url,
                result=record.result,
            )
        )
    await update.effective_chat.send_message(
        "\n".join(lines), parse_mode=ParseMode.MARKDOWN
    )


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return
    if not await _check_force_join(update, context):
        return
    user_id = update.effective_user.id
    language = await _get_language(context, user_id)
    prefs = await _database(context).get_user_preferences(user_id)
    text, keyboard = render_settings_view(language, prefs)
    await update.effective_chat.send_message(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message or not update.effective_user:
        return
    if not await _check_force_join(update, context):
        return
    language = await _get_language(context, update.effective_user.id)
    urls = extract_urls(update.effective_message.text or "")
    if not urls:
        return
    await _handle_scan(update, context, urls, language)


async def _handle_scan(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    urls: List[str],
    language: str,
) -> None:
    user = update.effective_user
    database = _database(context)
    phishtank = _phishtank(context)
    config = _config(context)
    await database.upsert_user(user.id, user.username)

    today = datetime.now(timezone.utc)
    prefs = await database.get_user_preferences(user.id)
    daily_limit = prefs.get("daily_scan_limit") or config.default_daily_limit
    daily_count = await database.daily_scan_count(user.id, today)
    remaining = max(daily_limit - daily_count, 0)
    if remaining <= 0:
        await update.effective_chat.send_message(
            get_string("daily_limit_reached", language, limit=daily_limit)
        )
        return

    for url in urls:
        if remaining <= 0:
            await update.effective_chat.send_message(
                get_string("daily_limit_reached", language, limit=daily_limit)
            )
            break
        await update.effective_chat.send_message(
            get_string("processing_url", language, url=url)
        )
        data = await phishtank.check_url(url)
        if data is None:
            await update.effective_chat.send_message(
                get_string("scan_error", language)
            )
            continue
        result = "phishing" if data.get("in_database") else "safe"
        verified = bool(data.get("verified"))
        detail_url = data.get("phish_detail_page") or data.get("detail_url")
        response_text = (
            get_string("scan_phishing", language)
            if result == "phishing"
            else get_string("scan_safe", language)
        )
        if data.get("cached"):
            response_text += f"\n{get_string('scan_cached', language)}"
        if detail_url:
            response_text += f"\n{detail_url}"
        await update.effective_chat.send_message(response_text)
        await database.log_scan(user.id, url, result, verified, detail_url)
        await database.increment_scan_stats(user.id, result=result, username=user.username)
        remaining -= 1


def build_user_handlers() -> List:
    """Return handlers for user commands and messages."""
    return [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("scan", scan),
        CommandHandler("stats", stats),
        CommandHandler("history", history),
        CommandHandler("settings", settings),
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text),
    ]
