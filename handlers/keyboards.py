"""Inline keyboard builders used across handlers."""

from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.strings import get_text


def build_main_menu_keyboard(user_lang: str) -> InlineKeyboardMarkup:
    """Build the main menu keyboard with quick actions."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(get_text(user_lang, 'menu_scan_button'), callback_data='menu_scan'),
            InlineKeyboardButton(get_text(user_lang, 'menu_stats_button'), callback_data='menu_stats')
        ],
        [
            InlineKeyboardButton(get_text(user_lang, 'menu_history_button'), callback_data='menu_history'),
            InlineKeyboardButton(get_text(user_lang, 'menu_settings_button'), callback_data='menu_settings')
        ],
        [
            InlineKeyboardButton(get_text(user_lang, 'menu_help_button'), callback_data='menu_help')
        ],
        [
            InlineKeyboardButton(get_text(user_lang, 'menu_contact_button'), callback_data='contact_manager')
        ],
        [
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data='lang_fa')
        ]
    ])


def build_settings_keyboard(user_lang: str) -> InlineKeyboardMarkup:
    """Build the settings keyboard for toggles and language."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data='lang_fa')
        ],
        [
            InlineKeyboardButton("🔔 Notifications", callback_data='toggle_notif'),
            InlineKeyboardButton("💡 Tips", callback_data='toggle_tips')
        ],
        [
            InlineKeyboardButton(get_text(user_lang, 'menu_main_button'), callback_data='menu_main')
        ]
    ])


def build_default_keyboard(user_lang: str) -> InlineKeyboardMarkup:
    """Keyboard shown on informational messages."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_text(user_lang, 'menu_main_button'), callback_data='menu_main')],
        [InlineKeyboardButton(get_text(user_lang, 'menu_contact_button'), callback_data='contact_manager')]
    ])


def build_join_keyboard(user_lang: str, channel_username: Optional[str] = None) -> InlineKeyboardMarkup:
    """Keyboard used when forcing the user to join a channel."""
    buttons = []

    if channel_username:
        url = f"https://t.me/{channel_username.lstrip('@')}"
        buttons.append([InlineKeyboardButton(get_text(user_lang, 'open_channel_button'), url=url)])

    buttons.append([InlineKeyboardButton(get_text(user_lang, 'join_button'), callback_data='check_join')])
    buttons.append([InlineKeyboardButton(get_text(user_lang, 'menu_main_button'), callback_data='menu_main')])

    return InlineKeyboardMarkup(buttons)


def with_default_keyboard(user_lang: str, reply_markup: Optional[InlineKeyboardMarkup] = None) -> InlineKeyboardMarkup:
    """Ensure a reply markup is always present."""
    return reply_markup if reply_markup else build_default_keyboard(user_lang)
