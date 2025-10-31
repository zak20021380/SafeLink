"""
Admin command handlers for SafeClick bot
Handles admin panel, broadcast, force join, and user management
"""

import asyncio
import time
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import Forbidden, BadRequest

from bot.database import db
from bot.strings import get_text
from bot.config import ADMIN_IDS

logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command - Show admin panel"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        prefs = db.get_user_preferences(user_id)
        user_lang = prefs.get('language', 'en') if prefs else 'en'
        await update.message.reply_text(get_text(user_lang, 'not_admin'))
        return

    # Get global stats
    global_stats = db.get_global_stats()

    # Get force join status
    force_join = "✅ Enabled" if db.is_force_join_enabled() else "❌ Disabled"
    channel_id, channel_username = db.get_force_join_channel()
    channel = channel_username if channel_username else "Not set"

    # Get global limit
    global_limit = db.get_global_daily_limit()

    admin_text = get_text(
        'en',  # Admin panel always in English
        'admin_panel',
        total_users=global_stats.get('total_users', 0) or 0,
        total_scans=global_stats.get('total_scans', 0) or 0,
        total_phishing=global_stats.get('total_phishing', 0) or 0,
        total_safe=global_stats.get('total_safe', 0) or 0,
        force_join=force_join,
        channel=channel,
        global_limit=global_limit
    )

    keyboard = [
        [
            InlineKeyboardButton("📊 Refresh Stats", callback_data='admin_refresh'),
        ]
    ]

    await update.message.reply_text(
        admin_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command - Send message to all users"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    if not context.args:
        await update.message.reply_text(
            get_text('en', 'broadcast_usage'),
            parse_mode='Markdown'
        )
        return

    message = ' '.join(context.args)
    user_ids = db.get_all_user_ids()

    # Confirm broadcast
    confirm_text = get_text(
        'en',
        'broadcast_confirm',
        count=len(user_ids),
        message=message
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Send", callback_data=f'broadcast_yes'),
            InlineKeyboardButton("❌ Cancel", callback_data='broadcast_no')
        ]
    ]

    # Store message in context for later use
    context.user_data['broadcast_message'] = message

    await update.message.reply_text(
        confirm_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def do_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    """Actually perform the broadcast"""
    user_ids = db.get_all_user_ids()
    total = len(user_ids)
    success = 0
    failed = 0

    start_time = time.time()

    # Send initial status
    status_msg = await update.callback_query.message.reply_text(
        get_text('en', 'broadcasting', sent=0, total=total, success=0, failed=0),
        parse_mode='Markdown'
    )

    # Broadcast to all users
    for i, uid in enumerate(user_ids, 1):
        try:
            await context.bot.send_message(chat_id=uid, text=message, parse_mode='Markdown')
            success += 1
        except Forbidden:
            # User blocked the bot
            failed += 1
            logger.info(f"User {uid} blocked the bot")
        except Exception as e:
            failed += 1
            logger.error(f"Error sending to {uid}: {e}")

        # Update status every 10 users
        if i % 10 == 0:
            try:
                await status_msg.edit_text(
                    get_text('en', 'broadcasting', sent=i, total=total, success=success, failed=failed),
                    parse_mode='Markdown'
                )
            except:
                pass

        # Small delay to avoid rate limits
        await asyncio.sleep(0.05)

    elapsed_time = int(time.time() - start_time)

    # Final status
    await status_msg.edit_text(
        get_text('en', 'broadcast_complete', total=total, success=success, failed=failed, time=elapsed_time),
        parse_mode='Markdown'
    )


async def forcejoin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /forcejoin command - Enable force join with channel"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            get_text('en', 'force_join_usage'),
            parse_mode='Markdown'
        )
        return

    channel_id = context.args[0]
    channel_username = context.args[1]

    # Validate channel username
    if not channel_username.startswith('@'):
        await update.message.reply_text("❌ Channel username must start with @")
        return

    # Enable force join
    db.enable_force_join(channel_id, channel_username)

    await update.message.reply_text(
        get_text('en', 'force_join_enabled', channel=channel_username),
        parse_mode='Markdown'
    )


async def disableforcejoin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /disableforcejoin command"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    db.disable_force_join()

    await update.message.reply_text(
        get_text('en', 'force_join_disabled'),
        parse_mode='Markdown'
    )


async def setlimit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setlimit command - Set custom limit for user"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage: `/setlimit <user_id> <limit>`\n\nExample: `/setlimit 123456789 100`",
            parse_mode='Markdown'
        )
        return

    try:
        target_user_id = int(context.args[0])
        limit = int(context.args[1])

        if limit < 0:
            await update.message.reply_text("❌ Limit must be positive!")
            return

        db.set_user_daily_limit(target_user_id, limit)

        await update.message.reply_text(
            get_text('en', 'limit_set', limit=limit, user_id=target_user_id),
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID or limit!")


async def setgloballimit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setgloballimit command - Set default limit for all users"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: `/setgloballimit <limit>`\n\nExample: `/setgloballimit 50`",
            parse_mode='Markdown'
        )
        return

    try:
        limit = int(context.args[0])

        if limit < 0:
            await update.message.reply_text("❌ Limit must be positive!")
            return

        db.set_global_daily_limit(limit)

        await update.message.reply_text(
            get_text('en', 'global_limit_set', limit=limit),
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid limit!")


async def resetlimit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resetlimit command - Reset user's limit to global default"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: `/resetlimit <user_id>`\n\nExample: `/resetlimit 123456789`",
            parse_mode='Markdown'
        )
        return

    try:
        target_user_id = int(context.args[0])

        db.reset_user_limit(target_user_id)
        global_limit = db.get_global_daily_limit()

        await update.message.reply_text(
            get_text('en', 'limit_reset', limit=global_limit, user_id=target_user_id),
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID!")


async def userinfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /userinfo command - View user information"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: `/userinfo <user_id>`\n\nExample: `/userinfo 123456789`",
            parse_mode='Markdown'
        )
        return

    try:
        target_user_id = int(context.args[0])

        stats = db.get_user_stats(target_user_id)
        if not stats:
            await update.message.reply_text(f"❌ User {target_user_id} not found in database!")
            return

        today_scans = db.get_today_scan_count(target_user_id)
        daily_limit = db.get_user_daily_limit(target_user_id)

        info_text = get_text(
            'en',
            'user_info',
            username=stats.get('username', 'N/A'),
            user_id=target_user_id,
            daily_limit=daily_limit,
            today_scans=today_scans,
            total_scans=stats.get('total_scans', 0),
            phishing_found=stats.get('phishing_found', 0)
        )

        await update.message.reply_text(info_text, parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID!")