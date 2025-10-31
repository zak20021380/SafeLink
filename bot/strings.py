"""
Bilingual strings for SafeClick bot
Supports English and Persian (Farsi)
"""

STRINGS = {
    'en': {
        # Welcome and Help
        'welcome': "🛡️ **Welcome to SafeClick!**\n\n"
                   "I protect you from phishing and malicious links.\n\n"
                   "**Your Stats:**\n"
                   "✅ Total scans: {total_scans}\n"
                   "🚨 Phishing found: {phishing_found}\n"
                   "🔍 Safe links: {safe_found}\n\n"
                   "Send me a link to scan!",

        'help': "🔍 **How to Use SafeClick:**\n\n"
                "**Commands:**\n"
                "/start - Start & view stats\n"
                "/help - Show this help\n"
                "/scan <url> - Scan a link\n"
                "/stats - Your statistics\n"
                "/history - Recent scans\n"
                "/settings - Preferences\n\n"
                "Or just send me any link!",

        # Stats
        'stats': "📊 **Your Statistics**\n\n"
                 "👤 User: @{username}\n"
                 "🆔 ID: `{user_id}`\n\n"
                 "📈 **Activity:**\n"
                 "✅ Total scans: {total_scans}\n"
                 "🚨 Phishing detected: {phishing_found}\n"
                 "🔒 Safe links: {safe_found}\n"
                 "❌ Errors: {errors}\n\n"
                 "📅 Member since: {first_seen}\n"
                 "🕐 Last active: {last_active}\n\n"
                 "📊 Today's scans: {today_scans}/{daily_limit}",

        # Scanning
        'scanning': "🔍 Scanning URL...\n`{url}`",
        'safe_link': "✅ **Link Appears Safe**\n\n"
                     "Our automated checks did not detect any malicious behaviour.\n\n"
                     "**Scan summary:**\n"
                     "• No phishing indicators were triggered during analysis.\n"
                     "• Threat intelligence sources currently consider this URL low risk.\n\n"
                     "⚠️ Always verify the sender before sharing personal data.\n"
                     "📨 You can send another link anytime for a fresh review.",
        'phishing_detected': "🚨 **HIGH RISK: PHISHING DETECTED**\n\n"
                             "The scan flagged this URL as malicious and unsafe to open.\n\n"
                             "**Why it is dangerous:**\n"
                             "• The content shows strong signs of credential theft or malware delivery.\n"
                             "• The domain or hosting matches known phishing infrastructure.\n\n"
                             "❌ Do not open, share, or submit any information on this site.\n"
                             "📨 Send a different link if you need it checked.",
        'error_scanning': "❌ **Error Scanning URL**\n\n{error}",
        'no_urls_found': "❌ I couldn't detect a valid link in your message.\n\n"
                          "Please send the full address including https:// or use /scan <url>.",
        'invalid_url_format': "❌ The link format looks incorrect.\n\n"
                               "Make sure it starts with http:// or https:// and try again.",
        'ready_for_links': "🔁 I'm ready for the next link whenever you are. Just paste it here!",
        'join_success': "✅ You're all set! You can now use the bot to analyse links.",

        # Limits
        'daily_limit_reached': "⚠️ **Daily Scan Limit Reached**\n\n"
                               "You've used {count}/{limit} scans today.\n"
                               "Limit resets at midnight UTC.\n\n"
                               "Contact admin for higher limits.",

        # History
        'history': "📜 **Recent Scan History**\n\n{history}\n\nShowing last {count} scans.",
        'no_history': "📭 No scan history yet.\n\nStart by sending me a URL!",

        # Settings
        'settings': "⚙️ **Your Settings**\n\n"
                    "🌐 Language: {language}\n"
                    "🔔 Notifications: {notifications}\n"
                    "📊 Daily limit: {daily_limit}\n"
                    "💡 Tips: {show_tips}",

        'language_changed': "✅ Language changed to English",
        'notifications_on': "🔔 Notifications enabled",
        'notifications_off': "🔕 Notifications disabled",
        'tips_on': "💡 Tips enabled",
        'tips_off': "💡 Tips disabled",

        # Force Join
        'join_channel': "📢 **Join Our Channel First!**\n\n"
                        "To use this bot, please join:\n"
                        "👉 {channel}\n\n"
                        "After joining, click the button below:",
        'join_button': "✅ I Joined",
        'not_joined': "❌ You haven't joined yet!\n\nPlease join: {channel}",

        # Admin
        'admin_panel': "👨‍💼 **Admin Panel**\n\n"
                       "**Statistics:**\n"
                       "👥 Total users: {total_users}\n"
                       "🔍 Total scans: {total_scans}\n"
                       "🚨 Phishing found: {total_phishing}\n"
                       "✅ Safe links: {total_safe}\n\n"
                       "**Settings:**\n"
                       "📢 Force join: {force_join}\n"
                       "📱 Channel: {channel}\n"
                       "📊 Global daily limit: {global_limit}\n\n"
                       "Use admin commands.",

        'broadcast_usage': "📢 **Broadcast Message**\n\n"
                           "Use `/broadcast` to enter interactive mode or `/broadcast <message>` for a quick text blast.\n\n"
                           "You can send text, photos, videos, or documents and they will be copied to every user.",

        'broadcast_prompt': "📢 **Broadcast Mode**\n\n"
                            "Send the exact message you want to deliver to all users.\n"
                            "You can forward or create a new message with any media.\n\n"
                            "Use the cancel button below to abort.",

        'broadcast_ready': "✅ Message saved!\n\nReview the preview below and confirm to send it to everyone.",

        'broadcast_confirm': "📢 **Confirm Broadcast**\n\n"
                             "Send to {count} users?\n\n{preview}",

        'broadcasting': "📤 Broadcasting...\n\n{sent}/{total}\n✅ Sent: {success}\n❌ Failed: {failed}",
        'broadcast_complete': "✅ **Broadcast Complete!**\n\nTotal: {total}\n✅ Sent: {success}\n❌ Failed: {failed}",
        'broadcast_cancelled': "❌ Broadcast cancelled.",

        'force_join_enabled': "✅ Force join enabled!\n\nChannel: {channel}",
        'force_join_disabled': "❌ Force join disabled!",
        'force_join_usage': "Usage: /forcejoin <channel_id> <@username>\n\nExample: `/forcejoin -1001234567890 @YourChannel`",

        'force_join_prompt': "📢 **Force Join Setup**\n\n"
                              "Current status: {status}\n"
                              "Channel: {channel}\n\n"
                              "Forward a message from the target channel or send its public @username.\n"
                              "Once I verify access, I'll enable force join.",
        'force_join_invalid': "❌ I couldn't detect a channel. Please forward a message from the desired channel or send its @username (e.g. @MyChannel).",
        'force_join_need_username': "❌ That channel doesn't have a public @username. Please set one in Telegram or send the @username manually.",
        'force_join_bot_not_admin': "❌ I am not an administrator in that channel. Add me as an admin and try again.",
        'force_join_cancelled': "❌ Force join setup cancelled.",

        'limit_set': "✅ Daily limit set to {limit} for user {user_id}",
        'global_limit_set': "✅ Global daily limit set to {limit}",
        'limit_reset': "✅ Limit reset to default ({limit}) for user {user_id}",
        'user_info': "📋 **User Info**\n\n"
                     "👤 Username: @{username}\n"
                     "🆔 ID: `{user_id}`\n"
                     "📊 Daily limit: {daily_limit}\n"
                     "📈 Today's scans: {today_scans}\n"
                     "✅ Total scans: {total_scans}\n"
                     "🚨 Phishing found: {phishing_found}",

        'not_admin': "❌ This command is for administrators only.",
    },

    'fa': {
        # Welcome and Help
        'welcome': "🛡️ **به SafeClick خوش آمدید!**\n\n"
                   "من شما را از لینک‌های فیشینگ محافظت می‌کنم.\n\n"
                   "**آمار شما:**\n"
                   "✅ کل اسکن‌ها: {total_scans}\n"
                   "🚨 فیشینگ یافت شده: {phishing_found}\n"
                   "🔍 لینک‌های امن: {safe_found}\n\n"
                   "یک لینک برای اسکن بفرستید!",

        'help': "🔍 **راهنمای استفاده:**\n\n"
                "**دستورات:**\n"
                "/start - شروع و مشاهده آمار\n"
                "/help - نمایش راهنما\n"
                "/scan <url> - اسکن لینک\n"
                "/stats - آمار شما\n"
                "/history - اسکن‌های اخیر\n"
                "/settings - تنظیمات\n\n"
                "یا مستقیم لینک بفرستید!",

        # Stats
        'stats': "📊 **آمار شما**\n\n"
                 "👤 کاربر: @{username}\n"
                 "🆔 شناسه: `{user_id}`\n\n"
                 "📈 **فعالیت:**\n"
                 "✅ کل اسکن‌ها: {total_scans}\n"
                 "🚨 فیشینگ شناسایی شده: {phishing_found}\n"
                 "🔒 لینک‌های امن: {safe_found}\n"
                 "❌ خطاها: {errors}\n\n"
                 "📅 عضویت از: {first_seen}\n"
                 "🕐 آخرین فعالیت: {last_active}\n\n"
                 "📊 اسکن‌های امروز: {today_scans}/{daily_limit}",

        # Scanning
        'scanning': "🔍 در حال اسکن...\n`{url}`",
        'safe_link': "✅ **لینک امن به نظر می‌رسد**\n\n"
                     "در بررسی خودکار، نشانه‌ای از فعالیت مخرب مشاهده نشد.\n\n"
                     "**خلاصه اسکن:**\n"
                     "• هیچ شاخص فیشینگی در محتوا فعال نشد.\n"
                     "• منابع تهدید این آدرس را کم‌خطر گزارش کرده‌اند.\n\n"
                     "⚠️ همیشه قبل از وارد کردن اطلاعات، فرستنده را بررسی کنید.\n"
                     "📨 هر زمان خواستید، لینک دیگری بفرستید تا بررسی شود.",
        'phishing_detected': "🚨 **هشدار جدی: فیشینگ شناسایی شد**\n\n"
                             "اسکن نشان می‌دهد این لینک مخرب و ناامن است.\n\n"
                             "**دلایل خطرناک بودن:**\n"
                             "• محتوا نشانه‌های قوی سرقت اطلاعات یا انتشار بدافزار دارد.\n"
                             "• دامنه یا میزبانی با زیرساخت‌های شناخته‌شده فیشینگ مطابقت دارد.\n\n"
                             "❌ به هیچ عنوان وارد لینک نشوید یا اطلاعاتی ارسال نکنید.\n"
                             "📨 برای بررسی، لینک دیگری بفرستید.",
        'error_scanning': "❌ **خطا در اسکن**\n\n{error}",
        'no_urls_found': "❌ لینکی با فرمت معتبر پیدا نکردم.\n\n"
                          "لطفا آدرس کامل را همراه با https:// بفرستید یا از ‎/scan استفاده کنید.",
        'invalid_url_format': "❌ فرمت لینک درست نیست.\n\n"
                               "لطفا لینک را با http:// یا https:// ارسال کنید و دوباره تلاش کنید.",
        'ready_for_links': "🔁 هر زمان آماده بودید، لینک بعدی را برای بررسی بفرستید.",
        'join_success': "✅ همه چیز آماده است! حالا می‌توانید لینک‌ها را با ربات بررسی کنید.",

        # Limits
        'daily_limit_reached': "⚠️ **محدودیت روزانه تمام شد**\n\n"
                               "شما {count}/{limit} اسکن امروز انجام داده‌اید.\n"
                               "محدودیت نیمه‌شب ریست می‌شود.\n\n"
                               "با ادمین تماس بگیرید.",

        # History
        'history': "📜 **تاریخچه اسکن‌ها**\n\n{history}\n\nنمایش {count} اسکن آخر.",
        'no_history': "📭 تاریخچه‌ای ندارید.\n\nیک لینک بفرستید!",

        # Settings
        'settings': "⚙️ **تنظیمات شما**\n\n"
                    "🌐 زبان: {language}\n"
                    "🔔 اعلان‌ها: {notifications}\n"
                    "📊 محدودیت روزانه: {daily_limit}\n"
                    "💡 نکات: {show_tips}",

        'language_changed': "✅ زبان به فارسی تغییر کرد",
        'notifications_on': "🔔 اعلان‌ها فعال شد",
        'notifications_off': "🔕 اعلان‌ها غیرفعال شد",
        'tips_on': "💡 نکات فعال شد",
        'tips_off': "💡 نکات غیرفعال شد",

        # Force Join
        'join_channel': "📢 **ابتدا در کانال عضو شوید!**\n\n"
                        "برای استفاده از ربات:\n"
                        "👉 {channel}\n\n"
                        "بعد از عضویت دکمه زیر را بزنید:",
        'join_button': "✅ عضو شدم",
        'not_joined': "❌ هنوز عضو نشدید!\n\nلطفا عضو شوید: {channel}",

        # Admin
        'admin_panel': "👨‍💼 **پنل ادمین**\n\n"
                       "**آمار:**\n"
                       "👥 کل کاربران: {total_users}\n"
                       "🔍 کل اسکن‌ها: {total_scans}\n"
                       "🚨 فیشینگ یافت شده: {total_phishing}\n"
                       "✅ لینک‌های امن: {total_safe}\n\n"
                       "**تنظیمات:**\n"
                       "📢 عضویت اجباری: {force_join}\n"
                       "📱 کانال: {channel}\n"
                       "📊 محدودیت پیش‌فرض: {global_limit}\n\n"
                       "از دستورات ادمین استفاده کنید.",

        'broadcast_usage': "📢 **ارسال پیام همگانی**\n\n"
                           "برای حالت تعاملی از `/broadcast` و برای متن سریع از `/broadcast <پیام>` استفاده کنید.\n\n"
                           "می‌توانید متن، عکس، ویدیو یا فایل ارسال کنید تا برای همه کاربران کپی شود.",

        'broadcast_prompt': "📢 **حالت ارسال همگانی**\n\n"
                            "پیامی که باید برای همه کاربران ارسال شود را بفرستید.\n"
                            "می‌توانید پیام جدید بسازید یا از کانال/چت دلخواه فوروارد کنید.\n\n"
                            "برای انصراف از دکمه لغو استفاده کنید.",

        'broadcast_ready': "✅ پیام ذخیره شد!\n\nپیش‌نمایش را بررسی و برای ارسال تایید کنید.",

        'broadcast_confirm': "📢 **تایید ارسال**\n\n"
                             "به {count} کاربر ارسال شود؟\n\n{preview}",

        'broadcasting': "📤 در حال ارسال...\n\n{sent}/{total}\n✅ ارسال شده: {success}\n❌ خطا: {failed}",
        'broadcast_complete': "✅ **ارسال کامل شد!**\n\nکل: {total}\n✅ ارسال شده: {success}\n❌ خطا: {failed}",
        'broadcast_cancelled': "❌ ارسال همگانی لغو شد.",

        'force_join_enabled': "✅ عضویت اجباری فعال شد!\n\nکانال: {channel}",
        'force_join_disabled': "❌ عضویت اجباری غیرفعال شد!",
        'force_join_usage': "نحوه استفاده: /forcejoin <شناسه_کانال> <@نام_کاربری>\n\nمثال: `/forcejoin -1001234567890 @YourChannel`",

        'force_join_prompt': "📢 **تنظیم عضویت اجباری**\n\n"
                              "وضعیت فعلی: {status}\n"
                              "کانال: {channel}\n\n"
                              "یک پیام از کانال موردنظر فوروارد کنید یا نام کاربری عمومی آن را بفرستید.\n"
                              "بعد از تایید دسترسی، عضویت اجباری فعال می‌شود.",
        'force_join_invalid': "❌ کانالی شناسایی نشد. لطفا یک پیام از کانال فوروارد کنید یا نام کاربری آن را به صورت @Example بفرستید.",
        'force_join_need_username': "❌ این کانال نام کاربری عمومی ندارد. ابتدا در تلگرام نام کاربری تعریف کنید یا آن را به صورت دستی بفرستید.",
        'force_join_bot_not_admin': "❌ ربات در این کانال ادمین نیست. ابتدا ربات را ادمین کنید و دوباره تلاش کنید.",
        'force_join_cancelled': "❌ تنظیم عضویت اجباری لغو شد.",

        'limit_set': "✅ محدودیت روزانه {limit} برای کاربر {user_id} تنظیم شد",
        'global_limit_set': "✅ محدودیت پیش‌فرض {limit} تنظیم شد",
        'limit_reset': "✅ محدودیت به پیش‌فرض ({limit}) برگشت برای کاربر {user_id}",
        'user_info': "📋 **اطلاعات کاربر**\n\n"
                     "👤 نام کاربری: @{username}\n"
                     "🆔 شناسه: `{user_id}`\n"
                     "📊 محدودیت روزانه: {daily_limit}\n"
                     "📈 اسکن‌های امروز: {today_scans}\n"
                     "✅ کل اسکن‌ها: {total_scans}\n"
                     "🚨 فیشینگ یافت شده: {phishing_found}",

        'not_admin': "❌ این دستور فقط برای ادمین‌هاست.",
    }
}


def get_text(user_lang: str, key: str, **kwargs) -> str:
    """
    Get localized text for user

    Args:
        user_lang: User's language ('en' or 'fa')
        key: String key
        **kwargs: Format parameters

    Returns:
        Formatted localized string
    """
    lang = user_lang if user_lang in STRINGS else 'en'
    text = STRINGS[lang].get(key, STRINGS['en'].get(key, f'Missing: {key}'))

    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError as e:
            return f"{text} (Missing param: {e})"

    return text