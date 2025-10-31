"""Callback query handlers for SafeClick."""
from __future__ import annotations

import logging
from typing import List, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes

from bot.strings import get_string

LOGGER = logging.getLogger(__name__)


def render_settings_view(language: str, prefs: dict) -> Tuple[str, InlineKeyboardMarkup]:
    """Return settings text and keyboard for the given language and prefs."""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_string(
                        "settings_notifications",
                        language,
                        status=_status(language, prefs.get("notifications", True)),
                    ),
                    callback_data="toggle_notifications",
                )
            ],
            [
                InlineKeyboardButton(
                    get_string(
                        "settings_tips",
                        language,
                        status=_status(language, prefs.get("show_tips", True)),
                    ),
                    callback_data="toggle_tips",
                )
            ],
            [
                InlineKeyboardButton(
                    get_string("settings_language", language, language=language),
                    callback_data="noop",
                ),
                InlineKeyboardButton("English", callback_data="lang_en"),
                InlineKeyboardButton("فارسی", callback_data="lang_fa"),
            ],
        ]
    )
    text = (
        get_string("settings_header", language)
        + "\n"
        + get_string(
            "settings_daily_limit",
            language,
            limit=prefs.get("daily_scan_limit", 50),
        )
    )
    return text, keyboard


def _status(language: str, value: bool) -> str:
    return get_string("toggle_on" if value else "toggle_off", language)


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.from_user:
        return
    await query.answer()
    language = "en" if query.data == "lang_en" else "fa"
    database = context.application.bot_data["database"]
    await database.update_user_preferences(query.from_user.id, language=language)
    prefs = await database.get_user_preferences(query.from_user.id)
    language = prefs.get("language", language)
    if query.message and query.message.text and "⚙️" in query.message.text:
        text, keyboard = render_settings_view(language, prefs)
        await query.edit_message_text(
            text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN
        )
    else:
        await query.edit_message_text(
            get_string("language_updated", language, language=language),
            parse_mode=ParseMode.MARKDOWN,
        )
    LOGGER.debug("Language updated for user %s to %s", query.from_user.id, language)


async def toggle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.from_user:
        return
    await query.answer()
    key = "notifications" if query.data == "toggle_notifications" else "show_tips"
    database = context.application.bot_data["database"]
    prefs = await database.get_user_preferences(query.from_user.id)
    new_value = not bool(prefs.get(key, True))
    await database.update_user_preferences(query.from_user.id, **{key: new_value})
    prefs = await database.get_user_preferences(query.from_user.id)
    language = prefs.get("language", "en")
    text, keyboard = render_settings_view(language, prefs)
    await query.edit_message_text(
        text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN
    )
    LOGGER.debug("Preference %s toggled for user %s", key, query.from_user.id)


async def noop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.answer()


def build_callback_handlers() -> List:
    return [
        CallbackQueryHandler(language_callback, pattern=r"^lang_(?:en|fa)$"),
        CallbackQueryHandler(toggle_callback, pattern=r"^toggle_(?:notifications|tips)$"),
        CallbackQueryHandler(noop_callback, pattern=r"^noop$"),
    ]


__all__ = [
    "render_settings_view",
    "language_callback",
    "toggle_callback",
    "noop_callback",
    "build_callback_handlers",
]
