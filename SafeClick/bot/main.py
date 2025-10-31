"""Entry point and application builder for SafeClick."""
from __future__ import annotations

import asyncio
import logging
from typing import Optional

from telegram.ext import AIORateLimiter, Application, ApplicationBuilder

from .config import Config, LOG_DIR
from .database import Database
from .utils import PhishTankClient, ensure_cache_cleanup
from handlers import build_admin_handlers, build_callback_handlers, build_user_handlers

LOGGER = logging.getLogger(__name__)


def _setup_logging(log_level: int) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / "safeclick.log"
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )


async def build_application(config: Optional[Config] = None) -> Application:
    """Build the Telegram application with all handlers."""
    if config is None:
        config = Config.from_env()
    _setup_logging(config.log_level)
    database = Database(config.database_path)
    await database.init()
    phishtank = PhishTankClient(config.phishtank_api_key, database)

    application = (
        ApplicationBuilder()
        .token(config.bot_token)
        .rate_limiter(AIORateLimiter())
        .build()
    )

    application.bot_data["config"] = config
    application.bot_data["database"] = database
    application.bot_data["phishtank"] = phishtank

    for handler in build_user_handlers():
        application.add_handler(handler)
    for handler in build_admin_handlers():
        application.add_handler(handler)
    for handler in build_callback_handlers():
        application.add_handler(handler)

    application.add_error_handler(_error_handler)

    application.job_queue.run_repeating(
        _cleanup_job,
        interval=24 * 60 * 60,
        first=60,
        name="cache-cleanup",
    )

    return application


async def _cleanup_job(context) -> None:  # type: ignore[override]
    database: Database = context.application.bot_data["database"]
    await ensure_cache_cleanup(database)


async def _error_handler(update, context) -> None:  # type: ignore[override]
    LOGGER.exception("An error occurred while handling update %s", update, exc_info=context.error)


async def main() -> None:
    """Run the SafeClick bot."""
    config = Config.from_env()
    application = await build_application(config)
    await application.run_polling(stop_signals=None)


if __name__ == "__main__":
    asyncio.run(main())
