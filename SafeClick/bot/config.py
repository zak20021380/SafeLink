"""Configuration loader for SafeClick."""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


@dataclass
class Config:
    """Configuration values for the SafeClick bot."""

    bot_token: str
    admin_ids: List[int]
    phishtank_api_key: str
    database_path: Path
    force_join_exempt_ids: List[int]
    log_level: int
    default_daily_limit: int

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

        admin_ids_raw = os.getenv("ADMIN_IDS", "")
        admin_ids = [int(i.strip()) for i in admin_ids_raw.split(",") if i.strip()]
        if not admin_ids:
            raise RuntimeError("At least one ADMIN_IDS must be provided")

        phishtank_api_key = os.getenv("PHISHTANK_API_KEY", "")
        if not phishtank_api_key:
            logging.warning("PHISHTANK_API_KEY is empty; scans will be limited")

        db_path_str = os.getenv("DATABASE_PATH", str(DATA_DIR / "safeclick.sqlite3"))
        database_path = Path(db_path_str).expanduser().resolve()
        database_path.parent.mkdir(parents=True, exist_ok=True)

        exempt_ids_raw = os.getenv("FORCE_JOIN_EXEMPT_IDS", "")
        force_join_exempt_ids = [
            int(i.strip()) for i in exempt_ids_raw.split(",") if i.strip()
        ]

        log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_name, logging.INFO)

        default_daily_limit = int(os.getenv("DEFAULT_DAILY_LIMIT", "50"))

        return cls(
            bot_token=bot_token,
            admin_ids=admin_ids,
            phishtank_api_key=phishtank_api_key,
            database_path=database_path,
            force_join_exempt_ids=force_join_exempt_ids,
            log_level=log_level,
            default_daily_limit=default_daily_limit,
        )


__all__ = ["Config", "PROJECT_ROOT", "DATA_DIR", "LOG_DIR"]
