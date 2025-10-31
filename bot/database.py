"""
Database handler for SafeClick bot
SQLite database for user stats, scan history, preferences, and admin settings
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = None):
        """Initialize database with VPS-proof absolute path"""
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, 'data', 'safeclick.db')

        # Create data directory if doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.init_database()
        logger.info(f"📂 Database initialized: {self.db_path}")

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_scans INTEGER DEFAULT 0,
                phishing_found INTEGER DEFAULT 0,
                safe_found INTEGER DEFAULT 0,
                errors INTEGER DEFAULT 0
            )
        ''')

        # Scan history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                result TEXT NOT NULL,
                scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                verified TEXT,
                detail_url TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'en',
                notifications_enabled BOOLEAN DEFAULT 1,
                daily_scan_limit INTEGER,
                show_tips BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # Admin settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Initialize default admin settings
        cursor.execute('''
            INSERT OR IGNORE INTO admin_settings (setting_key, setting_value)
            VALUES 
                ('force_join_enabled', '0'),
                ('force_join_channel_id', ''),
                ('force_join_channel_username', ''),
                ('global_daily_limit', '5')
        ''')

        # Ensure legacy installations respect new 24-hour cap of 5 scans
        cursor.execute('''
            UPDATE admin_settings
            SET setting_value = '5'
            WHERE setting_key = 'global_daily_limit' AND CAST(setting_value AS INTEGER) > 5
        ''')

        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scan_history_user ON scan_history(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scan_history_date ON scan_history(scanned_at)')

        conn.commit()
        conn.close()
        logger.info("✅ Database tables created/verified")

    # ==================== USER MANAGEMENT ====================

    def add_user(self, user_id: int, username: str = None) -> bool:
        """Add new user or update existing user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
            exists = cursor.fetchone()

            if exists:
                cursor.execute('''
                    UPDATE users 
                    SET last_active = CURRENT_TIMESTAMP, username = ?
                    WHERE user_id = ?
                ''', (username, user_id))
            else:
                cursor.execute('''
                    INSERT INTO users (user_id, username)
                    VALUES (?, ?)
                ''', (user_id, username))

                cursor.execute('''
                    INSERT INTO user_preferences (user_id)
                    VALUES (?)
                ''', (user_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
            return False

    def get_user_stats(self, user_id: int) -> Optional[Dict]:
        """Get user statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()

            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return None

    def update_user_activity(self, user_id: int):
        """Update user's last active timestamp"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE users 
                SET last_active = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (user_id,))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error updating activity: {e}")

    # ==================== SCAN HISTORY ====================

    def add_scan(self, user_id: int, url: str, result: str,
                 verified: str = None, detail_url: str = None) -> bool:
        """Add scan to history and update user stats"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Add to history
            cursor.execute('''
                INSERT INTO scan_history 
                (user_id, url, result, verified, detail_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, url, result, verified, detail_url))

            # Update user stats
            if result == 'phishing':
                cursor.execute('''
                    UPDATE users 
                    SET total_scans = total_scans + 1,
                        phishing_found = phishing_found + 1,
                        last_active = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (user_id,))
            elif result == 'safe':
                cursor.execute('''
                    UPDATE users 
                    SET total_scans = total_scans + 1,
                        safe_found = safe_found + 1,
                        last_active = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (user_id,))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET total_scans = total_scans + 1,
                        errors = errors + 1,
                        last_active = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (user_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding scan: {e}")
            return False

    def get_user_scan_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's recent scan history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM scan_history 
                WHERE user_id = ?
                ORDER BY scanned_at DESC
                LIMIT ?
            ''', (user_id, limit))

            rows = cursor.fetchall()
            conn.close()

            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting scan history: {e}")
            return []

    def get_today_scan_count(self, user_id: int) -> int:
        """Get number of scans user performed today"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT COUNT(*) as count
                FROM scan_history
                WHERE user_id = ?
                AND scanned_at >= datetime('now', '-1 day')
            ''', (user_id,))

            result = cursor.fetchone()
            conn.close()

            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting today's scan count: {e}")
            return 0

    def search_scan_history(self, url: str, days: int = 1) -> Optional[Dict]:
        """Check if URL was scanned recently (caching)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM scan_history
                WHERE url = ?
                AND scanned_at >= datetime('now', '-' || ? || ' days')
                ORDER BY scanned_at DESC
                LIMIT 1
            ''', (url, days))

            row = cursor.fetchone()
            conn.close()

            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error searching scan history: {e}")
            return None

    # ==================== USER PREFERENCES ====================

    def get_user_preferences(self, user_id: int) -> Optional[Dict]:
        """Get user preferences"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return dict(row)
            else:
                self.add_user(user_id)
                return self.get_user_preferences(user_id)
        except Exception as e:
            logger.error(f"Error getting preferences: {e}")
            return None

    def update_language(self, user_id: int, language: str) -> bool:
        """Update user's language preference"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE user_preferences
                SET language = ?
                WHERE user_id = ?
            ''', (language, user_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating language: {e}")
            return False

    def update_notifications(self, user_id: int, enabled: bool) -> bool:
        """Update notification preference"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE user_preferences
                SET notifications_enabled = ?
                WHERE user_id = ?
            ''', (1 if enabled else 0, user_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating notifications: {e}")
            return False

    def toggle_tips(self, user_id: int) -> bool:
        """Toggle security tips"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE user_preferences
                SET show_tips = NOT show_tips
                WHERE user_id = ?
            ''', (user_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error toggling tips: {e}")
            return False

    def set_user_daily_limit(self, user_id: int, limit: int) -> bool:
        """Set custom daily limit for user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE user_preferences
                SET daily_scan_limit = ?
                WHERE user_id = ?
            ''', (limit, user_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error setting user limit: {e}")
            return False

    def reset_user_limit(self, user_id: int) -> bool:
        """Reset user limit to global default"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE user_preferences
                SET daily_scan_limit = NULL
                WHERE user_id = ?
            ''', (user_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error resetting user limit: {e}")
            return False

    def get_user_daily_limit(self, user_id: int) -> int:
        """Get user's daily scan limit (custom or global)"""
        try:
            prefs = self.get_user_preferences(user_id)
            limit = None
            if prefs and prefs.get('daily_scan_limit') is not None:
                limit = prefs['daily_scan_limit']

            if limit is None:
                global_limit = self.get_setting('global_daily_limit')
                limit = int(global_limit) if global_limit else 5

            # Every user is capped at 5 scans per rolling 24-hour window
            return min(limit, 5)
        except Exception as e:
            logger.error(f"Error getting user daily limit: {e}")
            return 5

    # ==================== ADMIN SETTINGS ====================

    def get_setting(self, key: str) -> Optional[str]:
        """Get admin setting"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT setting_value FROM admin_settings WHERE setting_key = ?', (key,))
            row = cursor.fetchone()
            conn.close()

            return row['setting_value'] if row else None
        except Exception as e:
            logger.error(f"Error getting setting: {e}")
            return None

    def set_setting(self, key: str, value: str) -> bool:
        """Set admin setting"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO admin_settings 
                (setting_key, setting_value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error setting: {e}")
            return False

    def is_force_join_enabled(self) -> bool:
        """Check if force join is enabled"""
        value = self.get_setting('force_join_enabled')
        return value == '1'

    def get_force_join_channel(self) -> Tuple[Optional[str], Optional[str]]:
        """Get force join channel ID and username"""
        channel_id = self.get_setting('force_join_channel_id')
        channel_username = self.get_setting('force_join_channel_username')
        return (channel_id, channel_username)

    def enable_force_join(self, channel_id: str, channel_username: str) -> bool:
        """Enable force join"""
        try:
            self.set_setting('force_join_enabled', '1')
            self.set_setting('force_join_channel_id', channel_id)
            self.set_setting('force_join_channel_username', channel_username)
            return True
        except Exception as e:
            logger.error(f"Error enabling force join: {e}")
            return False

    def disable_force_join(self) -> bool:
        """Disable force join"""
        return self.set_setting('force_join_enabled', '0')

    def set_global_daily_limit(self, limit: int) -> bool:
        """Set global daily scan limit"""
        enforced_limit = min(limit, 5)
        return self.set_setting('global_daily_limit', str(enforced_limit))

    def get_global_daily_limit(self) -> int:
        """Get global daily limit"""
        limit = self.get_setting('global_daily_limit')
        try:
            value = int(limit)
        except (TypeError, ValueError):
            value = 5
        return min(value, 5)

    # ==================== STATISTICS ====================

    def get_global_stats(self) -> Dict:
        """Get global statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT user_id) as total_users,
                    SUM(total_scans) as total_scans,
                    SUM(phishing_found) as total_phishing,
                    SUM(safe_found) as total_safe
                FROM users
            ''')

            row = cursor.fetchone()
            conn.close()

            return dict(row) if row else {}
        except Exception as e:
            logger.error(f"Error getting global stats: {e}")
            return {}

    def get_all_user_ids(self) -> List[int]:
        """Get all user IDs for broadcasting"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT user_id FROM users')
            rows = cursor.fetchall()
            conn.close()

            return [row['user_id'] for row in rows]
        except Exception as e:
            logger.error(f"Error getting all user IDs: {e}")
            return []


# Create singleton instance
db = Database()