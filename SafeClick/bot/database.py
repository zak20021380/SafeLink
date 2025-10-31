"""Database layer for SafeClick Telegram bot."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import aiosqlite

LOGGER = logging.getLogger(__name__)


@dataclass
class UserStats:
    """Dataclass representing user statistics."""

    user_id: int
    username: Optional[str]
    total_scans: int
    phishing_found: int
    safe_found: int
    first_seen: datetime
    last_active: datetime


@dataclass
class ScanRecord:
    """Dataclass representing a scan history entry."""

    user_id: int
    url: str
    result: str
    scanned_at: datetime
    verified: bool
    detail_url: Optional[str]


class Database:
    """Async SQLite database helper."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._lock = asyncio.Lock()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

    async def init(self) -> None:
        """Create all tables if they do not already exist."""
        async with self._connect() as db:
            await db.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    total_scans INTEGER NOT NULL DEFAULT 0,
                    phishing_found INTEGER NOT NULL DEFAULT 0,
                    safe_found INTEGER NOT NULL DEFAULT 0,
                    first_seen TEXT NOT NULL,
                    last_active TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS scan_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    url TEXT NOT NULL,
                    result TEXT NOT NULL,
                    scanned_at TEXT NOT NULL,
                    verified INTEGER NOT NULL DEFAULT 0,
                    detail_url TEXT,
                    UNIQUE(user_id, url, scanned_at)
                );

                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id INTEGER PRIMARY KEY,
                    language TEXT NOT NULL DEFAULT 'en',
                    notifications INTEGER NOT NULL DEFAULT 1,
                    daily_scan_limit INTEGER NOT NULL DEFAULT 50,
                    show_tips INTEGER NOT NULL DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS admin_settings (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    force_join_enabled INTEGER NOT NULL DEFAULT 0,
                    force_join_channel_id INTEGER,
                    force_join_channel_username TEXT
                );

                INSERT OR IGNORE INTO admin_settings (id) VALUES (1);

                CREATE TABLE IF NOT EXISTS url_cache (
                    url TEXT PRIMARY KEY,
                    result TEXT NOT NULL,
                    detail_url TEXT,
                    verified INTEGER NOT NULL DEFAULT 0,
                    cached_at TEXT NOT NULL
                );
                """
            )
            await db.commit()

    async def _connect(self) -> aiosqlite.Connection:
        return await aiosqlite.connect(self._db_path.as_posix())

    async def upsert_user(self, user_id: int, username: Optional[str]) -> None:
        """Insert or update a user record."""
        now = datetime.now(timezone.utc).isoformat()
        async with self._lock:
            async with self._connect() as db:
                await db.execute(
                    """
                    INSERT INTO user_stats (user_id, username, first_seen, last_active)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        username=excluded.username,
                        last_active=excluded.last_active
                    """,
                    (user_id, username, now, now),
                )
                await db.execute(
                    """
                    INSERT OR IGNORE INTO user_preferences (user_id)
                    VALUES (?)
                    """,
                    (user_id,),
                )
                await db.commit()

    async def increment_scan_stats(
        self, user_id: int, *, result: str, username: Optional[str]
    ) -> None:
        """Increment statistics for a scan result."""
        now = datetime.now(timezone.utc).isoformat()
        phishing_increment = 1 if result == "phishing" else 0
        safe_increment = 1 if result == "safe" else 0
        async with self._lock:
            async with self._connect() as db:
                await db.execute(
                    """
                    UPDATE user_stats
                    SET total_scans = total_scans + 1,
                        phishing_found = phishing_found + ?,
                        safe_found = safe_found + ?,
                        username = COALESCE(?, username),
                        last_active = ?
                    WHERE user_id = ?
                    """,
                    (phishing_increment, safe_increment, username, now, user_id),
                )
                await db.commit()

    async def log_scan(
        self,
        user_id: int,
        url: str,
        result: str,
        verified: bool,
        detail_url: Optional[str],
    ) -> None:
        """Log a scan into history."""
        async with self._lock:
            async with self._connect() as db:
                await db.execute(
                    """
                    INSERT INTO scan_history (user_id, url, result, scanned_at, verified, detail_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        url,
                        result,
                        datetime.now(timezone.utc).isoformat(),
                        int(verified),
                        detail_url,
                    ),
                )
                await db.commit()

    async def get_user_stats(self, user_id: int) -> Optional[UserStats]:
        """Retrieve stats for a user."""
        async with self._connect() as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM user_stats WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
        if row is None:
            return None
        return UserStats(
            user_id=row["user_id"],
            username=row["username"],
            total_scans=row["total_scans"],
            phishing_found=row["phishing_found"],
            safe_found=row["safe_found"],
            first_seen=datetime.fromisoformat(row["first_seen"]),
            last_active=datetime.fromisoformat(row["last_active"]),
        )

    async def get_recent_history(self, user_id: int, limit: int = 10) -> List[ScanRecord]:
        """Return recent scan history for a user."""
        async with self._connect() as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT user_id, url, result, scanned_at, verified, detail_url
                FROM scan_history
                WHERE user_id = ?
                ORDER BY datetime(scanned_at) DESC
                LIMIT ?
                """,
                (user_id, limit),
            ) as cursor:
                rows = await cursor.fetchall()
        return [
            ScanRecord(
                user_id=row["user_id"],
                url=row["url"],
                result=row["result"],
                scanned_at=datetime.fromisoformat(row["scanned_at"]),
                verified=bool(row["verified"]),
                detail_url=row["detail_url"],
            )
            for row in rows
        ]

    async def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user preferences, returning defaults if missing."""
        async with self._connect() as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM user_preferences WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
        if row is None:
            return {
                "language": "en",
                "notifications": True,
                "daily_scan_limit": 50,
                "show_tips": True,
            }
        return {
            "language": row["language"],
            "notifications": bool(row["notifications"]),
            "daily_scan_limit": row["daily_scan_limit"],
            "show_tips": bool(row["show_tips"]),
        }

    async def update_user_preferences(self, user_id: int, **kwargs: Any) -> None:
        """Update user preferences with provided keyword arguments."""
        allowed = {"language", "notifications", "daily_scan_limit", "show_tips"}
        columns = []
        values: List[Any] = []
        for key, value in kwargs.items():
            if key not in allowed:
                raise ValueError(f"Invalid preference key: {key}")
            columns.append(f"{key} = ?")
            if key in {"notifications", "show_tips"}:
                value = int(bool(value))
            values.append(value)
        if not columns:
            return
        values.append(user_id)
        query = f"UPDATE user_preferences SET {', '.join(columns)} WHERE user_id = ?"
        async with self._lock:
            async with self._connect() as db:
                await db.execute(query, tuple(values))
                await db.commit()

    async def get_admin_settings(self) -> Dict[str, Any]:
        """Return the admin settings row."""
        async with self._connect() as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM admin_settings WHERE id = 1") as cursor:
                row = await cursor.fetchone()
        if row is None:
            return {
                "force_join_enabled": False,
                "force_join_channel_id": None,
                "force_join_channel_username": None,
            }
        return {
            "force_join_enabled": bool(row["force_join_enabled"]),
            "force_join_channel_id": row["force_join_channel_id"],
            "force_join_channel_username": row["force_join_channel_username"],
        }

    async def set_force_join(
        self,
        *,
        enabled: bool,
        channel_id: Optional[int] = None,
        channel_username: Optional[str] = None,
    ) -> None:
        """Update force join settings."""
        async with self._lock:
            async with self._connect() as db:
                await db.execute(
                    """
                    UPDATE admin_settings
                    SET force_join_enabled = ?,
                        force_join_channel_id = ?,
                        force_join_channel_username = ?
                    WHERE id = 1
                    """,
                    (int(enabled), channel_id, channel_username),
                )
                await db.commit()

    async def get_all_user_ids(self) -> List[int]:
        """Return a list of all user IDs."""
        async with self._connect() as db:
            async with db.execute("SELECT user_id FROM user_stats") as cursor:
                rows = await cursor.fetchall()
        return [row[0] for row in rows]

    async def get_global_stats(self) -> Dict[str, int]:
        """Return aggregate statistics across all users."""
        async with self._connect() as db:
            async with db.execute(
                "SELECT COUNT(*), COALESCE(SUM(total_scans), 0),"
                " COALESCE(SUM(phishing_found), 0), COALESCE(SUM(safe_found), 0)"
                " FROM user_stats"
            ) as cursor:
                row = await cursor.fetchone()
        user_count = row[0] if row else 0
        total_scans = row[1] if row else 0
        phishing_found = row[2] if row else 0
        safe_found = row[3] if row else 0
        return {
            "user_count": user_count,
            "total_scans": total_scans,
            "phishing_found": phishing_found,
            "safe_found": safe_found,
        }

    async def cache_url_result(
        self, url: str, result: str, *, verified: bool, detail_url: Optional[str]
    ) -> None:
        """Cache the result of a URL lookup for 24 hours."""
        async with self._lock:
            async with self._connect() as db:
                await db.execute(
                    """
                    INSERT INTO url_cache (url, result, detail_url, verified, cached_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(url) DO UPDATE SET
                        result=excluded.result,
                        detail_url=excluded.detail_url,
                        verified=excluded.verified,
                        cached_at=excluded.cached_at
                    """,
                    (
                        url,
                        result,
                        detail_url,
                        int(verified),
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
                await db.commit()

    async def get_cached_url_result(
        self, url: str, *, max_age: timedelta
    ) -> Optional[Tuple[str, bool, Optional[str]]]:
        """Return cached result if younger than max_age."""
        async with self._connect() as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT result, verified, detail_url, cached_at FROM url_cache WHERE url = ?",
                (url,),
            ) as cursor:
                row = await cursor.fetchone()
        if row is None:
            return None
        cached_at = datetime.fromisoformat(row["cached_at"])
        if datetime.now(timezone.utc) - cached_at > max_age:
            return None
        return (row["result"], bool(row["verified"]), row["detail_url"])

    async def daily_scan_count(self, user_id: int, day: datetime) -> int:
        """Return count of scans by user for specific day (UTC)."""
        start = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
        end = start + timedelta(days=1)
        async with self._connect() as db:
            async with db.execute(
                """
                SELECT COUNT(*) FROM scan_history
                WHERE user_id = ?
                    AND datetime(scanned_at) >= ?
                    AND datetime(scanned_at) < ?
                """,
                (user_id, start.isoformat(), end.isoformat()),
            ) as cursor:
                row = await cursor.fetchone()
        return row[0] if row else 0

    async def purge_old_cache(self, *, older_than: timedelta) -> None:
        """Remove stale cache entries."""
        threshold = datetime.now(timezone.utc) - older_than
        async with self._lock:
            async with self._connect() as db:
                await db.execute(
                    "DELETE FROM url_cache WHERE datetime(cached_at) < ?",
                    (threshold.isoformat(),),
                )
                await db.commit()

