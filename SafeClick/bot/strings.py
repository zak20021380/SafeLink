"""Bilingual strings for SafeClick bot."""
from __future__ import annotations

from typing import Dict

SUPPORTED_LANGUAGES = ("en", "fa")

STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        "start_welcome": "👋 Welcome to SafeClick!\nUse /scan <url> or send a link to begin.",
        "start_stats": "Total scans: {total_scans}\nPhishing detected: {phishing_found}\nSafe links: {safe_found}",
        "choose_language": "Please choose your preferred language:",
        "help": (
            "🔍 *SafeClick Help*\n"
            "• /scan <url> — Scan a specific link\n"
            "• /stats — Show your statistics\n"
            "• /history — View your last 10 scans\n"
            "• /settings — Configure preferences\n"
            "Just send a message containing up to 3 links to scan them automatically."
        ),
        "no_url_found": "I couldn't find a valid URL in your message.",
        "processing_url": "Scanning {url}…",
        "scan_safe": "✅ This link is not reported as phishing.",
        "scan_phishing": "🚨 Warning! This link is reported as phishing.",
        "scan_error": "⚠️ An error occurred while checking this link. Please try again later.",
        "stats_message": (
            "📊 *Your stats*\nTotal scans: {total_scans}\n"
            "Phishing detected: {phishing_found}\nSafe links: {safe_found}\n"
            "First seen: {first_seen}\nLast active: {last_active}"
        ),
        "history_header": "🗂️ *Recent scans*",
        "history_item": "{scanned_at}: {url} → {result}",
        "history_empty": "You have no scans yet. Try /scan <url>!",
        "settings_header": "⚙️ *Settings*",
        "settings_notifications": "Notifications: {status}",
        "settings_tips": "Safety tips: {status}",
        "settings_language": "Language: {language}",
        "settings_daily_limit": "Daily scan limit: {limit}",
        "toggle_on": "ON",
        "toggle_off": "OFF",
        "language_updated": "Language updated to {language}.",
        "preference_updated": "Your settings have been updated.",
        "daily_limit_reached": "You have reached your daily scan limit of {limit} URLs.",
        "admin_only": "This command is restricted to administrators.",
        "admin_panel": "🛡️ *Admin panel*\nUsers: {user_count}\nTotal scans: {total_scans}",
        "broadcast_prompt": "Please provide a message to broadcast.",
        "broadcast_confirm": "Broadcasting to {count} users…",
        "broadcast_done": "Broadcast completed successfully.",
        "force_join_enabled": "Force join enabled for {channel}.",
        "force_join_disabled": "Force join has been disabled.",
        "force_join_required": "Please join {channel} to use the bot.",
        "invalid_arguments": "Invalid arguments provided.",
        "scan_cached": "(cached result)",
        "phishtank_error": "PhishTank API error: {error}",
    },
    "fa": {
        "start_welcome": "👋 به سیف‌کلیک خوش آمدید!\nبرای شروع /scan <url> را بفرستید یا لینک ارسال کنید.",
        "start_stats": "تعداد اسکن‌ها: {total_scans}\nفیشینگ شناسایی شده: {phishing_found}\nلینک‌های امن: {safe_found}",
        "choose_language": "لطفاً زبان مورد نظر خود را انتخاب کنید:",
        "help": (
            "🔍 *راهنمای سیف‌کلیک*\n"
            "• ‎/scan <url> — اسکن یک لینک\n"
            "• ‎/stats — نمایش آمار شما\n"
            "• ‎/history — نمایش ۱۰ اسکن اخیر\n"
            "• ‎/settings — تنظیمات کاربری\n"
            "همچنین می‌توانید حداکثر ۳ لینک را در یک پیام ارسال کنید تا به صورت خودکار اسکن شوند."
        ),
        "no_url_found": "هیچ لینک معتبری در پیام شما پیدا نکردم.",
        "processing_url": "در حال بررسی {url}…",
        "scan_safe": "✅ این لینک به عنوان فیشینگ گزارش نشده است.",
        "scan_phishing": "🚨 هشدار! این لینک به عنوان فیشینگ گزارش شده است.",
        "scan_error": "⚠️ هنگام بررسی لینک خطایی رخ داد. لطفاً بعداً دوباره امتحان کنید.",
        "stats_message": (
            "📊 *آمار شما*\nتعداد اسکن‌ها: {total_scans}\n"
            "فیشینگ شناسایی شده: {phishing_found}\nلینک‌های امن: {safe_found}\n"
            "اولین استفاده: {first_seen}\nآخرین فعالیت: {last_active}"
        ),
        "history_header": "🗂️ *اسکن‌های اخیر*",
        "history_item": "{scanned_at}: {url} → {result}",
        "history_empty": "هنوز لینکی را اسکن نکرده‌اید. /scan <url> را امتحان کنید!",
        "settings_header": "⚙️ *تنظیمات*",
        "settings_notifications": "اعلان‌ها: {status}",
        "settings_tips": "نکات ایمنی: {status}",
        "settings_language": "زبان: {language}",
        "settings_daily_limit": "حداکثر اسکن روزانه: {limit}",
        "toggle_on": "فعال",
        "toggle_off": "غیرفعال",
        "language_updated": "زبان به {language} تغییر کرد.",
        "preference_updated": "تنظیمات شما به‌روزرسانی شد.",
        "daily_limit_reached": "به سقف روزانه {limit} لینک رسیده‌اید.",
        "admin_only": "این دستور فقط برای مدیران مجاز است.",
        "admin_panel": "🛡️ *پنل مدیریت*\nکاربران: {user_count}\nمجموع اسکن‌ها: {total_scans}",
        "broadcast_prompt": "لطفاً پیام ارسالی برای همه کاربران را وارد کنید.",
        "broadcast_confirm": "در حال ارسال برای {count} کاربر…",
        "broadcast_done": "ارسال همگانی با موفقیت انجام شد.",
        "force_join_enabled": "الزام عضویت در {channel} فعال شد.",
        "force_join_disabled": "الزام عضویت غیرفعال شد.",
        "force_join_required": "لطفاً برای استفاده از ربات عضو {channel} شوید.",
        "invalid_arguments": "آرگومان‌های نامعتبر ارسال شده‌اند.",
        "scan_cached": "(نتیجه ذخیره‌شده)",
        "phishtank_error": "خطای سرویس PhishTank: {error}",
    },
}


def get_string(key: str, language: str = "en", **kwargs: str) -> str:
    """Return a localized string for the given key."""
    if language not in STRINGS:
        language = "en"
    template = STRINGS[language].get(key, STRINGS["en"].get(key, key))
    return template.format(**kwargs)


__all__ = ["SUPPORTED_LANGUAGES", "STRINGS", "get_string"]
