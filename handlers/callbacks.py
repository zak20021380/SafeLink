"""
Callback query handlers for SafeClick bot
Handles all inline button clicks
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.database import db
from bot.strings import get_text
from bot.config import ADMIN_IDS
from .admin_commands import do_broadcast, is_admin, start_broadcast_flow, start_forcejoin_flow
from .user_commands import (
    build_main_menu_keyboard,
    build_settings_keyboard,
    SUPPORT_STATE_KEY,
    SUPPORT_THREADS_KEY,
    SUPPORT_REPLY_STATE,
    _format_safe
)

logger = logging.getLogger(__name__)


async def _send_ready_message(query, lang: str):
    """Send a reminder that user can submit another link."""
    try:
        await query.message.reply_text(
            get_text(lang, 'ready_for_links'),
            parse_mode='Markdown'
        )
    except Exception as exc:
        logger.debug(f"Unable to send ready message: {exc}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    await query.answer()

    db.update_user_activity(user_id)

    prefs = db.get_user_preferences(user_id)
    user_lang = prefs.get('language', 'en') if prefs else 'en'

    # ==================== LANGUAGE SELECTION ====================

    if data.startswith('lang_'):
        lang = data.split('_')[1]
        db.update_language(user_id, lang)

        await query.edit_message_text(
            get_text(lang, 'language_changed'),
            parse_mode='Markdown'
        )
        await _send_ready_message(query, lang)
        await query.message.reply_text(
            get_text(lang, 'menu_prompt'),
            reply_markup=build_main_menu_keyboard(lang)
        )

    # ==================== SETTINGS TOGGLES ====================

    elif data == 'toggle_notif':
        current = prefs.get('notifications_enabled', True)
        new_state = not current
        db.update_notifications(user_id, new_state)

        msg = 'notifications_on' if new_state else 'notifications_off'
        await query.edit_message_text(get_text(user_lang, msg))
        await _send_ready_message(query, user_lang)

    elif data == 'toggle_tips':
        db.toggle_tips(user_id)
        prefs = db.get_user_preferences(user_id)  # Refresh

        msg = 'tips_on' if prefs.get('show_tips') else 'tips_off'
        await query.edit_message_text(get_text(user_lang, msg))
        await _send_ready_message(query, user_lang)

    # ==================== MAIN MENU ACTIONS ====================

    elif data == 'menu_scan':
        await query.message.reply_text(get_text(user_lang, 'menu_scan_desc'))

    elif data == 'menu_stats':
        stats = db.get_user_stats(user_id)
        today_scans = db.get_today_scan_count(user_id)
        daily_limit = db.get_user_daily_limit(user_id)

        if not stats:
            await query.message.reply_text("❌ Unable to load your stats right now.")
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

        await query.message.reply_text(stats_text, parse_mode='Markdown')

    elif data == 'menu_history':
        history = db.get_user_scan_history(user_id, limit=10)

        if not history:
            await query.message.reply_text(
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

        await query.message.reply_text(full_text, parse_mode='Markdown')

    elif data == 'menu_settings':
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

        await query.message.reply_text(
            settings_text,
            reply_markup=build_settings_keyboard(),
            parse_mode='Markdown'
        )

    elif data == 'menu_help':
        await query.message.reply_text(
            get_text(user_lang, 'help'),
            parse_mode='Markdown'
        )

    elif data == 'contact_manager':
        context.user_data.pop(SUPPORT_REPLY_STATE, None)
        context.user_data[SUPPORT_STATE_KEY] = True
        await query.message.reply_text(get_text(user_lang, 'contact_prompt'))

    elif data.startswith('support_reply:'):
        if not is_admin(user_id):
            await query.answer("❌ Admin only!", show_alert=True)
            return

        try:
            target_id = int(data.split(':')[1])
        except (IndexError, ValueError):
            await query.answer("❌ Invalid target.", show_alert=True)
            return

        threads = context.bot_data.get(SUPPORT_THREADS_KEY, {})
        info = threads.get(target_id)

        if not info:
            await query.answer(get_text('en', 'contact_unknown_thread'), show_alert=True)
            return

        context.user_data[SUPPORT_REPLY_STATE] = target_id
        display = info.get('display', str(target_id))
        prompt = get_text('en', 'contact_reply_prompt', display=_format_safe(display), user_id=target_id)

        await query.message.reply_text(prompt)

    # ==================== FORCE JOIN CHECK ====================

    elif data == 'check_join':
        # Check if user joined channel
        if not db.is_force_join_enabled():
            await query.edit_message_text(get_text(user_lang, 'join_success'))
            await _send_ready_message(query, user_lang)
            return

        channel_id, channel_username = db.get_force_join_channel()
        if not channel_id:
            await query.edit_message_text(get_text(user_lang, 'join_success'))
            await _send_ready_message(query, user_lang)
            return

        try:
            member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)

            if member.status in ['member', 'administrator', 'creator']:
                await query.edit_message_text(get_text(user_lang, 'join_success'))
                await _send_ready_message(query, user_lang)
            else:
                await query.answer(
                    get_text(user_lang, 'not_joined', channel=channel_username),
                    show_alert=True
                )
        except Exception as e:
            logger.error(f"Error checking membership: {e}")
            await query.edit_message_text(get_text(user_lang, 'join_success'))
            await _send_ready_message(query, user_lang)

    # ==================== ADMIN PANEL ACTIONS ====================

    elif data == 'admin_refresh':
        if not is_admin(user_id):
            await query.answer("❌ Admin only!", show_alert=True)
            return

        # Refresh admin panel stats
        global_stats = db.get_global_stats()
        force_join = "✅ Enabled" if db.is_force_join_enabled() else "❌ Disabled"
        channel_id, channel_username = db.get_force_join_channel()
        channel = channel_username if channel_username else "Not set"
        global_limit = db.get_global_daily_limit()

        admin_text = get_text(
            'en',
            'admin_panel',
            total_users=global_stats.get('total_users', 0) or 0,
            total_scans=global_stats.get('total_scans', 0) or 0,
            total_phishing=global_stats.get('total_phishing', 0) or 0,
            total_safe=global_stats.get('total_safe', 0) or 0,
            force_join=force_join,
            channel=channel,
            global_limit=global_limit
        )

        try:
            await query.edit_message_text(admin_text, parse_mode='Markdown', reply_markup=query.message.reply_markup)
            await query.answer("✅ Stats refreshed!")
        except:
            await query.answer("Already up to date!")

    elif data == 'admin_broadcast':
        if not is_admin(user_id):
            await query.answer("❌ Admin only!", show_alert=True)
            return

        await start_broadcast_flow(query.message, context)

    elif data == 'admin_forcejoin':
        if not is_admin(user_id):
            await query.answer("❌ Admin only!", show_alert=True)
            return

        await start_forcejoin_flow(query.message, context)

    # ==================== BROADCAST CONFIRMATION ====================

    elif data == 'broadcast_yes':
        if not is_admin(user_id):
            await query.answer("❌ Admin only!", show_alert=True)
            return

        if not context.user_data.get('broadcast_payload'):
            await query.edit_message_text(
                "❌ Broadcast message not found. Please use /broadcast again."
            )
            return

        await query.edit_message_text("📤 Starting broadcast...")
        await do_broadcast(update, context)

    elif data == 'broadcast_no':
        if not is_admin(user_id):
            await query.answer("❌ Admin only!", show_alert=True)
            return

        context.user_data.pop('broadcast_state', None)
        context.user_data.pop('broadcast_payload', None)
        await query.edit_message_text(
            get_text('en', 'broadcast_cancelled'),
            parse_mode='Markdown'
        )

    elif data == 'broadcast_cancel_flow':
        if not is_admin(user_id):
            await query.answer("❌ Admin only!", show_alert=True)
            return

        context.user_data.pop('broadcast_state', None)
        context.user_data.pop('broadcast_payload', None)
        await query.edit_message_text(
            get_text('en', 'broadcast_cancelled'),
            parse_mode='Markdown'
        )

    elif data == 'forcejoin_cancel':
        if not is_admin(user_id):
            await query.answer("❌ Admin only!", show_alert=True)
            return

        context.user_data.pop('forcejoin_state', None)
        await query.edit_message_text(
            get_text('en', 'force_join_cancelled'),
            parse_mode='Markdown'
        )

    # ==================== UNKNOWN CALLBACK ====================

    else:
        logger.warning(f"Unknown callback data: {data}")
        await query.answer("❌ Unknown action!")