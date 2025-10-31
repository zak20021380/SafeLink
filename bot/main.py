"""
SafeClick Bot - Main Entry Point
Telegram bot for phishing link detection

Complete professional bot with:
- User management & statistics
- Bilingual support (English & Persian)
- Admin panel with full control
- Force join channel
- Broadcast messages
- Daily scan limits
- Scan history tracking
"""

import logging
import os
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

# Import configuration
from bot.config import BOT_TOKEN, ADMIN_IDS
from bot.database import db

# Import handlers
from handlers.user_commands import (
    start_command,
    help_command,
    stats_command,
    history_command,
    settings_command,
    scan_command,
    handle_message
)
from handlers.admin_commands import (
    admin_command,
    broadcast_command,
    forcejoin_command,
    disableforcejoin_command,
    setlimit_command,
    setgloballimit_command,
    resetlimit_command,
    userinfo_command
)
from handlers.callbacks import button_callback

# Setup logging
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def error_handler(update, context):
    """Handle errors"""
    logger.error(f"Update {update} caused error: {context.error}")

    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again later."
            )
    except Exception as e:
        logger.error(f"Error in error handler: {e}")


def main():
    """Start the bot"""
    logger.info("=" * 60)
    logger.info("🛡️  SafeClick Bot - Phishing Link Detection")
    logger.info("=" * 60)
    logger.info("")

    # Validate configuration
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ BOT_TOKEN not set in .env file!")
        logger.error("   Please add your bot token from @BotFather")
        return

    if not ADMIN_IDS:
        logger.warning("⚠️  No ADMIN_IDS configured!")
        logger.warning("   Admin commands will not work")

    # Create application
    app = Application.builder().token(BOT_TOKEN).build()

    logger.info("📦 Registering handlers...")

    # ==================== USER COMMANDS ====================

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("scan", scan_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CommandHandler("settings", settings_command))

    logger.info("✅ User commands registered")

    # ==================== ADMIN COMMANDS ====================

    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("forcejoin", forcejoin_command))
    app.add_handler(CommandHandler("disableforcejoin", disableforcejoin_command))
    app.add_handler(CommandHandler("setlimit", setlimit_command))
    app.add_handler(CommandHandler("setgloballimit", setgloballimit_command))
    app.add_handler(CommandHandler("resetlimit", resetlimit_command))
    app.add_handler(CommandHandler("userinfo", userinfo_command))

    logger.info("✅ Admin commands registered")

    # ==================== MESSAGE HANDLERS ====================

    # Auto-scan messages with URLs
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    ))

    logger.info("✅ Message handlers registered")

    # ==================== CALLBACK HANDLERS ====================

    app.add_handler(CallbackQueryHandler(button_callback))

    logger.info("✅ Callback handlers registered")

    # ==================== ERROR HANDLER ====================

    app.add_error_handler(error_handler)

    logger.info("✅ Error handler registered")

    # ==================== BOT INFO ====================

    logger.info("")
    logger.info("=" * 60)
    logger.info("📊 Bot Configuration:")
    logger.info(f"   👨‍💼 Admins: {ADMIN_IDS}")
    logger.info(f"   📂 Database: {db.db_path}")
    logger.info(f"   🌐 Languages: English, Persian")
    logger.info(f"   📢 Force Join: {'Enabled' if db.is_force_join_enabled() else 'Disabled'}")
    logger.info(f"   📊 Global Limit: {db.get_global_daily_limit()} scans/day")
    logger.info("=" * 60)
    logger.info("")

    # ==================== START BOT ====================

    logger.info("🚀 Bot is starting...")
    logger.info("📱 Send /start to your bot on Telegram!")
    logger.info("")
    logger.info("💡 Commands:")
    logger.info("   User: /start /help /scan /stats /history /settings")
    logger.info("   Admin: /admin /broadcast /forcejoin /setlimit")
    logger.info("")
    logger.info("🛑 Press Ctrl+C to stop")
    logger.info("-" * 60)
    logger.info("")

    try:
        app.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 60)
        logger.info("👋 Bot stopped by user")
        logger.info("=" * 60)
    except Exception as e:
        logger.error("")
        logger.error("=" * 60)
        logger.error(f"❌ Fatal error: {e}")
        logger.error("=" * 60)
        raise


if __name__ == '__main__':
    main()