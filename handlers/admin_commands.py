"""
Admin command handlers for SafeClick bot
Handles admin panel, broadcast, force join, and user management
"""

import asyncio
import time
import logging
import re
from typing import Optional, Tuple

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes
from telegram.error import Forbidden, BadRequest
from telegram.helpers import escape_markdown

from bot.database import db
from bot.strings import get_text
from bot.config import ADMIN_IDS

logger = logging.getLogger(__name__)

BROADCAST_STATE_KEY = 'broadcast_state'
BROADCAST_PAYLOAD_KEY = 'broadcast_payload'
FORCEJOIN_STATE_KEY = 'forcejoin_state'


def _truncate(text: str, limit: int = 400) -> str:
    if not text:
        return ''
    text = text.strip()
    return text if len(text) <= limit else text[:limit - 1] + '…'


def _extract_username(text: str) -> Optional[str]:
    if not text:
        return None
    username_match = re.search(r'@([A-Za-z0-9_]{5,})', text)
    if username_match:
        return f"@{username_match.group(1)}"
    url_match = re.search(r'(?:t\.me|telegram\.me|telegram\.dog)/([A-Za-z0-9_]{5,})', text)
    if url_match:
        return f"@{url_match.group(1)}"
    return None


def _extract_channel_id(text: str) -> Optional[str]:
    if not text:
        return None
    match = re.search(r'-100\d{5,}', text)
    return match.group(0) if match else None


def _describe_message(message: Message) -> Tuple[str, str]:
    if message.text and not any([
        message.photo,
        message.video,
        message.document,
        message.animation,
        message.audio,
        message.voice,
        message.video_note,
        message.sticker
    ]):
        return "📝", "Text"
    if message.photo:
        return "🖼", "Photo"
    if message.video:
        return "🎬", "Video"
    if message.document:
        return "📄", "Document"
    if message.animation:
        return "🎞", "Animation"
    if message.audio:
        return "🎵", "Audio"
    if message.voice:
        return "🎙", "Voice message"
    if message.video_note:
        return "📹", "Video note"
    if message.sticker:
        return "🌟", "Sticker"
    if message.poll:
        return "🗳", "Poll"
    if message.location or message.venue:
        return "📍", "Location"
    if message.contact:
        return "👤", "Contact"
    if message.invoice or message.successful_payment:
        return "💳", "Payment"
    return "🔁", "Forwarded message"


def _build_broadcast_preview(payload: Optional[dict] = None, message: Optional[Message] = None) -> str:
    if payload and payload.get('mode') == 'text':
        return f"📝 Text\n{_truncate(payload.get('text', ''))}"
    if message:
        emoji, label = _describe_message(message)
        text = message.text or message.caption
        if text:
            return f"{emoji} {label}\n{_truncate(text)}"
        return f"{emoji} {label}"
    return "🔁 Forwarded message"


def _current_forcejoin_status() -> Tuple[str, str]:
    status = "✅ Enabled" if db.is_force_join_enabled() else "❌ Disabled"
    channel_id, channel_username = db.get_force_join_channel()
    channel_display = channel_username or (channel_id or "Not set")
    return status, channel_display


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
        [InlineKeyboardButton("📊 Refresh Stats", callback_data='admin_refresh')],
        [
            InlineKeyboardButton("📢 Broadcast", callback_data='admin_broadcast'),
            InlineKeyboardButton("📣 Force Join", callback_data='admin_forcejoin')
        ]
    ]

    await update.message.reply_text(
        admin_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def _send_broadcast_confirmation(message: Message, context: ContextTypes.DEFAULT_TYPE,
                                       payload: dict, preview: str):
    """Send confirmation message for broadcast"""
    context.user_data[BROADCAST_PAYLOAD_KEY] = payload
    context.user_data[BROADCAST_STATE_KEY] = 'awaiting_confirm'

    await message.reply_text(
        get_text('en', 'broadcast_ready'),
        parse_mode='Markdown'
    )

    user_count = len(db.get_all_user_ids())
    preview_text = escape_markdown(preview, version=1)
    confirm_text = get_text('en', 'broadcast_confirm', count=user_count, preview=preview_text)

    keyboard = [
        [
            InlineKeyboardButton("✅ Send", callback_data='broadcast_yes'),
            InlineKeyboardButton("❌ Cancel", callback_data='broadcast_no')
        ]
    ]

    await message.reply_text(
        confirm_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def start_broadcast_flow(message: Message, context: ContextTypes.DEFAULT_TYPE):
    """Prompt admin to send the broadcast content"""
    context.user_data[BROADCAST_STATE_KEY] = 'awaiting_content'
    context.user_data.pop(BROADCAST_PAYLOAD_KEY, None)

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='broadcast_cancel_flow')]]

    await message.reply_text(
        get_text('en', 'broadcast_prompt'),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    if not context.args:
        await start_broadcast_flow(update.message, context)
        return

    message_text = ' '.join(context.args).strip()
    if not message_text:
        await update.message.reply_text(
            get_text('en', 'broadcast_usage'),
            parse_mode='Markdown'
        )
        return

    payload = {
        'mode': 'text',
        'text': message_text,
        'parse_mode': 'Markdown'
    }
    preview = _build_broadcast_preview(payload=payload)
    await _send_broadcast_confirmation(update.message, context, payload, preview)


async def do_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Actually perform the broadcast"""
    payload = context.user_data.get(BROADCAST_PAYLOAD_KEY)
    if not payload:
        await update.callback_query.message.edit_text(
            "❌ Broadcast payload missing. Please use /broadcast again."
        )
        return

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
            if payload.get('mode') == 'text':
                await context.bot.send_message(
                    chat_id=uid,
                    text=payload.get('text', ''),
                    parse_mode=payload.get('parse_mode')
                )
            else:
                await context.bot.copy_message(
                    chat_id=uid,
                    from_chat_id=payload.get('from_chat_id'),
                    message_id=payload.get('message_id')
                )
            success += 1
        except Forbidden:
            # User blocked the bot
            failed += 1
            logger.info(f"User {uid} blocked the bot")
        except BadRequest as e:
            failed += 1
            logger.error(f"BadRequest sending to {uid}: {e}")
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
            except Exception:
                pass

        # Small delay to avoid rate limits
        await asyncio.sleep(0.05)

    elapsed_time = int(time.time() - start_time)

    # Final status
    await status_msg.edit_text(
        get_text('en', 'broadcast_complete', total=total, success=success, failed=failed, time=elapsed_time),
        parse_mode='Markdown'
    )

    context.user_data.pop(BROADCAST_STATE_KEY, None)
    context.user_data.pop(BROADCAST_PAYLOAD_KEY, None)


async def start_forcejoin_flow(message: Message, context: ContextTypes.DEFAULT_TYPE):
    """Prompt admin to configure force join"""
    context.user_data[FORCEJOIN_STATE_KEY] = 'awaiting_channel'

    status, channel_display = _current_forcejoin_status()
    channel_display = escape_markdown(channel_display, version=1)

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='forcejoin_cancel')]]

    await message.reply_text(
        get_text('en', 'force_join_prompt', status=status, channel=channel_display),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def forcejoin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /forcejoin command - Enable force join with channel"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    if not context.args:
        await start_forcejoin_flow(update.message, context)
        return

    channel_id = None
    channel_username = None
    channel_title: Optional[str] = None

    for arg in context.args:
        if arg.startswith('@') or 't.me' in arg or 'telegram.' in arg:
            channel_username = _extract_username(arg)
        elif arg.startswith('-100') or arg.lstrip('-').isdigit():
            channel_id = arg

    if channel_username:
        channel_username = f"@{channel_username.lstrip('@')}"

    try:
        if channel_username and not channel_id:
            chat = await context.bot.get_chat(channel_username)
            channel_id = str(chat.id)
            channel_title = chat.title or channel_username
            if not chat.username:
                await update.message.reply_text(get_text('en', 'force_join_need_username'), parse_mode='Markdown')
                return
        elif channel_id and not channel_username:
            chat = await context.bot.get_chat(int(channel_id))
            if chat.username:
                channel_username = f"@{chat.username}"
            else:
                await update.message.reply_text(get_text('en', 'force_join_need_username'), parse_mode='Markdown')
                return
            channel_title = chat.title or channel_username
    except Exception as e:
        logger.error(f"Error resolving channel: {e}")
        await update.message.reply_text(get_text('en', 'force_join_invalid'), parse_mode='Markdown')
        return

    if not channel_id or not channel_username:
        await update.message.reply_text(
            get_text('en', 'force_join_usage'),
            parse_mode='Markdown'
        )
        return

    await _finalize_forcejoin(update.message, context, channel_id, channel_username, channel_title)


async def _finalize_forcejoin(message: Message, context: ContextTypes.DEFAULT_TYPE,
                              channel_id: str, channel_username: str,
                              channel_title: Optional[str] = None):
    """Validate and store force join settings"""
    try:
        bot_id = context.application.bot_data.get('bot_id') if context.application else None
        if not bot_id:
            bot = await context.bot.get_me()
            bot_id = bot.id
            if context.application:
                context.application.bot_data['bot_id'] = bot_id

        member = await context.bot.get_chat_member(chat_id=int(channel_id), user_id=bot_id)
        if member.status not in ('administrator', 'creator'):
            await message.reply_text(get_text('en', 'force_join_bot_not_admin'), parse_mode='Markdown')
            return
    except (Forbidden, BadRequest) as e:
        logger.error(f"Bot lacks admin rights for channel {channel_id}: {e}")
        await message.reply_text(get_text('en', 'force_join_bot_not_admin'), parse_mode='Markdown')
        return
    except Exception as e:
        logger.error(f"Error validating force join channel {channel_id}: {e}")
        await message.reply_text(get_text('en', 'force_join_invalid'), parse_mode='Markdown')
        return

    db.enable_force_join(str(channel_id), channel_username)
    context.user_data.pop(FORCEJOIN_STATE_KEY, None)

    display_name = channel_title or channel_username
    display_name = escape_markdown(display_name, version=1)

    await message.reply_text(
        get_text('en', 'force_join_enabled', channel=display_name),
        parse_mode='Markdown'
    )


async def _handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if context.user_data.get(BROADCAST_STATE_KEY) != 'awaiting_content':
        return False

    user_id = update.effective_user.id
    if not is_admin(user_id):
        return False

    db.update_user_activity(user_id)

    message = update.message
    payload = {
        'mode': 'copy',
        'from_chat_id': message.chat_id,
        'message_id': message.message_id
    }
    preview = _build_broadcast_preview(message=message)
    await _send_broadcast_confirmation(message, context, payload, preview)
    return True


async def _handle_forcejoin_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if context.user_data.get(FORCEJOIN_STATE_KEY) != 'awaiting_channel':
        return False

    user_id = update.effective_user.id
    if not is_admin(user_id):
        return False

    db.update_user_activity(user_id)

    message = update.message
    channel = message.forward_from_chat

    if channel and channel.type == 'channel':
        channel_id = str(channel.id)
        if channel.username:
            channel_username = f"@{channel.username}"
        else:
            await message.reply_text(get_text('en', 'force_join_need_username'), parse_mode='Markdown')
            return True
        channel_title = channel.title or channel_username
        await _finalize_forcejoin(message, context, channel_id, channel_username, channel_title)
        return True

    text = (message.text or '').strip()
    if not text:
        await message.reply_text(get_text('en', 'force_join_invalid'), parse_mode='Markdown')
        return True

    channel_username = _extract_username(text)
    channel_id = _extract_channel_id(text)
    channel_title = None

    try:
        if channel_username and not channel_id:
            chat = await context.bot.get_chat(channel_username)
            channel_id = str(chat.id)
            channel_title = chat.title or channel_username
            if not chat.username:
                await message.reply_text(get_text('en', 'force_join_need_username'), parse_mode='Markdown')
                return True
        elif channel_id and not channel_username:
            chat = await context.bot.get_chat(int(channel_id))
            if chat.username:
                channel_username = f"@{chat.username}"
            else:
                await message.reply_text(get_text('en', 'force_join_need_username'), parse_mode='Markdown')
                return True
            channel_title = chat.title or channel_username
    except Exception as e:
        logger.error(f"Error resolving channel during setup: {e}")
        await message.reply_text(get_text('en', 'force_join_invalid'), parse_mode='Markdown')
        return True

    if not channel_id or not channel_username:
        await message.reply_text(get_text('en', 'force_join_invalid'), parse_mode='Markdown')
        return True

    await _finalize_forcejoin(message, context, channel_id, channel_username, channel_title)
    return True


async def handle_admin_interactions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Handle pending admin interactive flows. Returns True if consumed."""
    if not update.message:
        return False

    user_id = update.effective_user.id
    if not is_admin(user_id):
        return False

    if await _handle_broadcast_message(update, context):
        return True

    if await _handle_forcejoin_message(update, context):
        return True

    return False


async def disableforcejoin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /disableforcejoin command"""
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text(get_text('en', 'not_admin'))
        return

    db.disable_force_join()
    context.user_data.pop(FORCEJOIN_STATE_KEY, None)

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