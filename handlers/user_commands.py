"""
User command handlers for SafeClick bot
Handles all user-facing commands and URL scanning
"""

import asyncio
import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.database import db
from bot.strings import get_text
from bot.utils import extract_urls, check_url, is_valid_url
from bot.config import ADMIN_IDS
from .admin_commands import handle_admin_interactions

logger = logging.getLogger(__name__)


async def check_force_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Check if user must join channel before using bot

    Returns:
        bool: True if user can proceed, False if must join
    """
    user_id = update.effective_user.id

    # Admins bypass force join
    if user_id in ADMIN_IDS:
        return True

    # Check if force join is enabled
    if not db.is_force_join_enabled():
        return True

    channel_id, channel_username = db.get_force_join_channel()
    if not channel_id:
        return True

    try:
        member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)

        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            # User not in channel
            prefs = db.get_user_preferences(user_id)
            user_lang = prefs.get('language', 'en') if prefs else 'en'

            keyboard = [[InlineKeyboardButton(
                get_text(user_lang, 'join_button'),
                callback_data='check_join'
            )]]

            await update.message.reply_text(
                get_text(user_lang, 'join_channel', channel=channel_username),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            return False
    except Exception as e:
        logger.error(f"Error checking channel membership: {e}")
        return True


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    user_id = user.id
    username = user.username

    # Add/update user in database
    db.add_user(user_id, username)

    # Check force join
    if not await check_force_join(update, context):
        return

    # Get user preferences and stats
    prefs = db.get_user_preferences(user_id)
    user_lang = prefs.get('language', 'en') if prefs else 'en'
    stats = db.get_user_stats(user_id)

    welcome_text = get_text(
        user_lang,
        'welcome',
        total_scans=stats.get('total_scans', 0) if stats else 0,
        phishing_found=stats.get('phishing_found', 0) if stats else 0,
        safe_found=stats.get('safe_found', 0) if stats else 0
    )

    # Language selection keyboard
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data='lang_fa')
        ]
    ]

    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user_id = update.effective_user.id
    db.update_user_activity(user_id)

    if not await check_force_join(update, context):
        return

    prefs = db.get_user_preferences(user_id)
    user_lang = prefs.get('language', 'en') if prefs else 'en'

    help_text = get_text(user_lang, 'help')
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    user_id = update.effective_user.id
    db.update_user_activity(user_id)

    if not await check_force_join(update, context):
        return

    stats = db.get_user_stats(user_id)
    prefs = db.get_user_preferences(user_id)
    user_lang = prefs.get('language', 'en') if prefs else 'en'
    today_scans = db.get_today_scan_count(user_id)
    daily_limit = db.get_user_daily_limit(user_id)

    if not stats:
        await update.message.reply_text("❌ Error getting your stats.")
        return

    stats_text = get_text(
        user_lang,
        'stats',
        username=stats.get('username', 'N/A'),
        user_id=user_id,
        total_scans=stats.get('total_scans', 0),
        phishing_found=stats.get('phishing_found', 0),
        safe_found=stats.get('safe_found', 0),
        errors=stats.get('errors', 0),
        first_seen=stats.get('first_seen', 'N/A')[:10],
        last_active=stats.get('last_active', 'N/A')[:10],
        today_scans=today_scans,
        daily_limit=daily_limit
    )

    await update.message.reply_text(stats_text, parse_mode='Markdown')


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /history command"""
    user_id = update.effective_user.id
    db.update_user_activity(user_id)

    if not await check_force_join(update, context):
        return

    prefs = db.get_user_preferences(user_id)
    user_lang = prefs.get('language', 'en') if prefs else 'en'

    history = db.get_user_scan_history(user_id, limit=10)

    if not history:
        await update.message.reply_text(
            get_text(user_lang, 'no_history'),
            parse_mode='Markdown'
        )
        return

    history_text = ""
    for i, scan in enumerate(history, 1):
        result_emoji = "🚨" if scan['result'] == 'phishing' else "✅" if scan['result'] == 'safe' else "❌"
        url_short = scan['url'][:40] + "..." if len(scan['url']) > 40 else scan['url']
        date = scan['scanned_at'][:10] if scan['scanned_at'] else 'N/A'
        history_text += f"{i}. {result_emoji} `{url_short}`\n   📅 {date}\n\n"

    full_text = get_text(
        user_lang,
        'history',
        history=history_text,
        count=len(history)
    )

    await update.message.reply_text(full_text, parse_mode='Markdown')


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    user_id = update.effective_user.id
    db.update_user_activity(user_id)

    if not await check_force_join(update, context):
        return

    prefs = db.get_user_preferences(user_id)
    user_lang = prefs.get('language', 'en') if prefs else 'en'
    daily_limit = db.get_user_daily_limit(user_id)

    settings_text = get_text(
        user_lang,
        'settings',
        language='🇮🇷 فارسی' if user_lang == 'fa' else '🇬🇧 English',
        notifications='ON' if prefs.get('notifications_enabled') else 'OFF',
        daily_limit=daily_limit,
        show_tips='ON' if prefs.get('show_tips') else 'OFF'
    )

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data='lang_fa')
        ],
        [
            InlineKeyboardButton("🔔 Notifications", callback_data='toggle_notif'),
            InlineKeyboardButton("💡 Tips", callback_data='toggle_tips')
        ]
    ]

    await update.message.reply_text(
        settings_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /scan command"""
    user_id = update.effective_user.id
    db.update_user_activity(user_id)

    if not await check_force_join(update, context):
        return

    prefs = db.get_user_preferences(user_id)
    user_lang = prefs.get('language', 'en') if prefs else 'en'

    # Check daily limit
    today_scans = db.get_today_scan_count(user_id)
    daily_limit = db.get_user_daily_limit(user_id)

    # Admins have unlimited scans
    if user_id not in ADMIN_IDS and today_scans >= daily_limit:
        await update.message.reply_text(
            get_text(user_lang, 'daily_limit_reached', count=today_scans, limit=daily_limit),
            parse_mode='Markdown'
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: `/scan https://example.com`",
            parse_mode='Markdown'
        )
        return

    url = context.args[0]

    if not is_valid_url(url):
        await update.message.reply_text(
            get_text(user_lang, 'invalid_url_format'),
            parse_mode='Markdown'
        )
        return
    await scan_url(update, url, user_id, user_lang)


async def scan_url(update, url: str, user_id: int, user_lang: str):
    """Scan a single URL and report results"""
    try:
        # Check cache first (avoid duplicate API calls)
        cached = db.search_scan_history(url, days=1)

        if cached:
            result_type = cached['result']
            verified = cached.get('verified')
            detail_url = cached.get('detail_url')
        else:
            # Send scanning message
            checking_msg = await update.message.reply_text(
                get_text(user_lang, 'scanning', url=url),
                parse_mode='Markdown'
            )

            # Check the URL using placeholder function
            result = check_url(url)

            if result.get('is_phishing') == True:
                result_type = 'phishing'
                verified = result.get('verified')
                detail_url = result.get('detail_url')

                response = get_text(user_lang, 'phishing_detected')
            elif result.get('is_phishing') == False:
                result_type = 'safe'
                verified = None
                detail_url = None
                response = get_text(user_lang, 'safe_link')
            else:
                result_type = 'error'
                verified = None
                detail_url = None
                error = result.get('error', 'Unknown error')
                response = get_text(user_lang, 'error_scanning', error=error)

            # Save to database
            db.add_scan(user_id, url, result_type, verified, detail_url)

            # Edit message with result
            await checking_msg.edit_text(response, parse_mode='Markdown')
            return

        # If cached, just show result
        if result_type == 'phishing':
            response = get_text(user_lang, 'phishing_detected')
        elif result_type == 'safe':
            response = get_text(user_lang, 'safe_link')
        else:
            response = get_text(user_lang, 'error_scanning', error='Cached error')

        await update.message.reply_text(response, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error scanning URL: {e}")
        await update.message.reply_text(
            get_text(user_lang, 'error_scanning', error=str(e)),
            parse_mode='Markdown'
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages containing URLs (auto-scan)"""
    user_id = update.effective_user.id
    if await handle_admin_interactions(update, context):
        return

    db.update_user_activity(user_id)

    if not await check_force_join(update, context):
        return

    text = update.message.text
    if not text:
        return

    prefs = db.get_user_preferences(user_id)
    user_lang = prefs.get('language', 'en') if prefs else 'en'

    urls = extract_urls(text)

    if not urls:
        # Notify user if message looks like an URL attempt but is invalid
        if re.search(r'(https?://|www\.)', text):
            await update.message.reply_text(
                get_text(user_lang, 'invalid_url_format'),
                parse_mode='Markdown'
            )
        return

    # Check daily limit
    today_scans = db.get_today_scan_count(user_id)
    daily_limit = db.get_user_daily_limit(user_id)

    # Admins have unlimited scans
    if user_id not in ADMIN_IDS and today_scans >= daily_limit:
        await update.message.reply_text(
            get_text(user_lang, 'daily_limit_reached', count=today_scans, limit=daily_limit),
            parse_mode='Markdown'
        )
        return

    # Scan URLs (limit to 3 per message)
    for url in urls[:3]:
        await scan_url(update, url, user_id, user_lang)
        if len(urls) > 1:
            await asyncio.sleep(1)  # Small delay between scans

    if len(urls) > 3:
        await update.message.reply_text(
            f"⚠️ Found {len(urls)} URLs, scanned first 3 to avoid rate limits."
        )