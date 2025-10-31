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
                   "Send me a link to scan!\n\n"
                   "⚠️ You can scan up to 5 links every 24 hours.",

        'menu_prompt': "📌 Choose an option below to continue:\n\n⚠️ Limit: 5 links every 24 hours.",
        'menu_scan_button': "🔍 Scan link",
        'menu_stats_button': "📊 My stats",
        'menu_history_button': "🕑 History",
        'menu_settings_button': "⚙️ Settings",
        'menu_help_button': "ℹ️ Help",
        'menu_contact_button': "📞 Contact manager",
        'menu_main_button': "🔙 Main menu",
        'menu_scan_desc': "🔍 Send me any link and I'll analyse it instantly. (Max 5 links per 24 hours)",

        'help': "🔍 **How to Use SafeClick:**\n\n"
                "**Commands:**\n"
                "/start - Start & view stats\n"
                "/help - Show this help\n"
                "/scan <url> - Scan a link\n"
                "/stats - Your statistics\n"
                "/history - Recent scans\n"
                "/settings - Preferences\n\n"
                "Or just send me any link!\n\n"
                "⚠️ Remember: only 5 links can be scanned every 24 hours.",

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
                 "📊 Today's scans (last 24h): {today_scans}/{daily_limit}\n"
                 "⚠️ Limit: 5 links every 24 hours",

        # Scanning
        'scanning': "🔍 Scanning URL...\n`{url}`\n\n⚠️ Only 5 links can be scanned every 24 hours.",
        'safe_link': "✅ **SafeClick Guardian AI Report**\n\n"
                     "SafeClick Guardian AI, powered by the SentinelNet threat intelligence cloud, completed an in-depth scan of:\n"
                     "`{url}`\n\n"
                     "**Result:** No malicious patterns were confirmed.\n"
                     "• Multi-layer heuristics and sandbox checks found no active phishing behaviour.\n"
                     "• SentinelNet currently classifies this domain as low risk across its global telemetry.\n\n"
                     "🧠 Engine: SafeClick Guardian AI\n"
                     "🗄️ Intelligence source: SentinelNet threat intelligence cloud\n\n"
                     "⚠️ Always verify the sender before sharing personal data.\n"
                     "📨 You can send another link anytime for a fresh review.\n\n"
                     "⏱️ Reminder: limit is 5 links per 24 hours.",
        'phishing_detected': "🚨 **HIGH RISK: PHISHING DETECTED**\n\n"
                             "SafeClick Guardian AI, backed by the SentinelNet threat intelligence cloud, has identified this URL as malicious.\n\n"
                             "**Why it is dangerous:**\n"
                             "• The content shows strong signs of credential theft or malware delivery.\n"
                             "• The domain or hosting matches known phishing infrastructure in SentinelNet's global database.\n\n"
                             "🧠 Engine: SafeClick Guardian AI\n"
                             "🗄️ Intelligence source: SentinelNet threat intelligence cloud\n\n"
                             "❌ Do not open, share, or submit any information on this site.\n"
                             "📨 Send a different link if you need it checked.\n\n"
                             "⏱️ Reminder: limit is 5 links per 24 hours.",
        'error_scanning': "❌ **Error Scanning URL**\n\n{error}\n\n⚠️ You can scan only 5 links every 24 hours.",
        'no_urls_found': "❌ I couldn't detect a valid link in your message.\n\n"
                          "Please send the full address including https:// or use /scan <url>.\n\n"
                          "⚠️ Limit reminder: 5 links every 24 hours.",
        'invalid_url_format': "❌ The link format looks incorrect.\n\n"
                               "Make sure it starts with http:// or https:// and try again.\n\n"
                               "⚠️ Limit reminder: 5 links every 24 hours.",
        'ready_for_links': "🔁 I'm ready for the next link whenever you are. Just paste it here!\n\n⚠️ Limit: 5 links per 24 hours.",
        'join_success': "✅ You're all set! You can now use the bot to analyse links.\n\n⚠️ Remember: 5 links every 24 hours.",

        # Contact Manager
        'contact_prompt': "📨 Please type your message for the manager. We'll notify them right away.",
        'contact_thanks': "✅ Your message was sent to the manager. They will reply here soon.",
        'contact_no_message': "❌ Please send a text message so we can forward it to the manager.",
        'contact_received_admin': "📩 New support message\n\nUser: {display}\nID: {user_id}\n\nMessage:\n{message}",
        'contact_reply_button': "✉️ Reply",
        'contact_reply_prompt': "💬 Replying to {display} (ID: {user_id}). Send your response now.",
        'contact_unknown_thread': "❌ Conversation not found. Ask the user to contact again.",
        'contact_reply_sent': "✅ Reply sent to the user.",
        'contact_reply_failed': "❌ Could not deliver the reply to the user.",
        'contact_reply_received': "📬 Manager reply:\n\n{message}\n\nYou can continue the conversation here.",

        # Limits
        'daily_limit_reached': "⚠️ **24-Hour Scan Limit Reached**\n\n"
                               "You've used {count}/{limit} scans in the last 24 hours (max 5).\n"
                               "Please wait until the 24-hour window resets before scanning again.\n\n"
                               "Contact admin if you need assistance.",

        # History
        'history': "📜 **Recent Scan History**\n\n{history}\n\nShowing last {count} scans.\n⚠️ Limit: 5 links every 24 hours.",
        'no_history': "📭 No scan history yet.\n\nStart by sending me a URL!",

        # Settings
        'settings': "⚙️ **Your Settings**\n\n"
                    "🌐 Language: {language}\n"
                    "🔔 Notifications: {notifications}\n"
                    "📊 Daily limit (24h): {daily_limit}\n"
                    "💡 Tips: {show_tips}\n\n"
                    "⚠️ Maximum of 5 scans every 24 hours.",

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
        'open_channel_button': "📢 Open channel",
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
                       "⚠️ Each user may scan only 5 links per 24-hour window.\n\n"
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

        'limit_set': "✅ Daily limit set to {limit} for user {user_id} (max 5 per 24h)",
        'global_limit_set': "✅ Global daily limit set to {limit} (capped at 5 per 24h)",
        'limit_reset': "✅ Limit reset to default ({limit}) for user {user_id} (max 5 per 24h)",
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
                   "یک لینک برای اسکن بفرستید!\n\n"
                   "⚠️ در هر ۲۴ ساعت فقط می‌توانید ۵ لینک را اسکن کنید.",

        'menu_prompt': "📌 برای ادامه یکی از گزینه‌های زیر را انتخاب کنید:\n\n⚠️ حداکثر ۵ لینک در هر ۲۴ ساعت قابل اسکن است.",
        'menu_scan_button': "🔍 اسکن لینک",
        'menu_stats_button': "📊 آمار من",
        'menu_history_button': "🕑 تاریخچه",
        'menu_settings_button': "⚙️ تنظیمات",
        'menu_help_button': "ℹ️ راهنما",
        'menu_contact_button': "📞 ارتباط با مدیر",
        'menu_main_button': "🔙 منوی اصلی",
        'menu_scan_desc': "🔍 هر لینکی را برایم بفرستید تا فوری بررسی کنم. (حداکثر ۵ لینک در ۲۴ ساعت)",

        'help': "🔍 **راهنمای استفاده:**\n\n"
                "**دستورات:**\n"
                "/start - شروع و مشاهده آمار\n"
                "/help - نمایش راهنما\n"
                "/scan <url> - اسکن لینک\n"
                "/stats - آمار شما\n"
                "/history - اسکن‌های اخیر\n"
                "/settings - تنظیمات\n\n"
                "یا مستقیم لینک بفرستید!\n\n"
                "⚠️ در هر بازه ۲۴ ساعته فقط ۵ لینک قابل اسکن است.",

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
                 "📊 اسکن‌های ۲۴ ساعت اخیر: {today_scans}/{daily_limit}\n"
                 "⚠️ حداکثر ۵ لینک در هر ۲۴ ساعت",

        # Scanning
        'scanning': "🔍 در حال اسکن...\n`{url}`\n\n⚠️ در هر ۲۴ ساعت فقط ۵ لینک قابل اسکن است.",
        'safe_link': "✅ **گزارش SafeClick Guardian AI**\n\n"
                     "هوش مصنوعی SafeClick Guardian با تکیه بر پایگاه تهدید قدرتمند SentinelNet اسکن عمیقی را برای لینک زیر به پایان رساند:\n"
                     "`{url}`\n\n"
                     "**نتیجه:** الگوی مخربی تأیید نشد.\n"
                     "• تحلیل چندلایه و آزمون‌های سندباکس هیچ نشانه فعال فیشینگ را آشکار نکرد.\n"
                     "• SentinelNet در پایش جهانی خود این دامنه را کم‌ریسک گزارش می‌کند.\n\n"
                     "🧠 موتور تحلیل: SafeClick Guardian AI\n"
                     "🗄️ منبع اطلاعاتی: پایگاه تهدید SentinelNet\n\n"
                     "⚠️ پیش از وارد کردن اطلاعات حساس، فرستنده را دوباره بررسی کنید.\n"
                     "📨 هر زمان مایل بودید، لینک دیگری بفرستید تا بررسی شود.\n\n"
                     "⏱️ یادآوری: حداکثر ۵ لینک در ۲۴ ساعت.",
        'phishing_detected': "🚨 **هشدار جدی: فیشینگ شناسایی شد**\n\n"
                             "هوش مصنوعی SafeClick Guardian با پشتیبانی پایگاه تهدید SentinelNet این لینک را مخرب و ناامن تشخیص داد.\n\n"
                             "**دلایل خطرناک بودن:**\n"
                             "• محتوا نشانه‌های قوی سرقت اطلاعات یا توزیع بدافزار را نشان می‌دهد.\n"
                             "• دامنه یا میزبانی با زیرساخت‌های شناخته‌شده فیشینگ در SentinelNet مطابقت دارد.\n\n"
                             "🧠 موتور تحلیل: SafeClick Guardian AI\n"
                             "🗄️ منبع اطلاعاتی: پایگاه تهدید SentinelNet\n\n"
                             "❌ به هیچ عنوان وارد لینک نشوید یا اطلاعاتی ارسال نکنید.\n"
                             "📨 برای بررسی، لینک دیگری بفرستید.\n\n"
                             "⏱️ یادآوری: حداکثر ۵ لینک در ۲۴ ساعت.",
        'error_scanning': "❌ **خطا در اسکن**\n\n{error}\n\n⚠️ توجه: در هر ۲۴ ساعت فقط ۵ لینک قابل اسکن است.",
        'no_urls_found': "❌ لینکی با فرمت معتبر پیدا نکردم.\n\n"
                          "لطفا آدرس کامل را همراه با https:// بفرستید یا از ‎/scan استفاده کنید.\n\n"
                          "⚠️ یادآوری محدودیت: ۵ لینک در هر ۲۴ ساعت.",
        'invalid_url_format': "❌ فرمت لینک درست نیست.\n\n"
                               "لطفا لینک را با http:// یا https:// ارسال کنید و دوباره تلاش کنید.\n\n"
                               "⚠️ یادآوری محدودیت: ۵ لینک در هر ۲۴ ساعت.",
        'ready_for_links': "🔁 هر زمان آماده بودید، لینک بعدی را برای بررسی بفرستید.\n\n⚠️ حداکثر ۵ لینک در ۲۴ ساعت.",
        'join_success': "✅ همه چیز آماده است! حالا می‌توانید لینک‌ها را با ربات بررسی کنید.\n\n⚠️ فراموش نکنید: ۵ لینک در هر ۲۴ ساعت.",

        # Contact Manager
        'contact_prompt': "📨 لطفاً پیام خود را برای مدیر بنویسید. بلافاصله به او اطلاع می‌دهیم.",
        'contact_thanks': "✅ پیام شما برای مدیر ارسال شد. به محض پاسخ، همینجا دریافت می‌کنید.",
        'contact_no_message': "❌ برای ارتباط با مدیر باید یک پیام متنی ارسال کنید.",
        'contact_received_admin': "📩 پیام جدید پشتیبانی\n\nکاربر: {display}\nشناسه: {user_id}\n\nمتن پیام:\n{message}",
        'contact_reply_button': "✉️ پاسخ",
        'contact_reply_prompt': "💬 در حال پاسخ به {display} (شناسه: {user_id}). پیام خود را ارسال کنید.",
        'contact_unknown_thread': "❌ مکالمه‌ای یافت نشد. از کاربر بخواهید دوباره پیام ارسال کند.",
        'contact_reply_sent': "✅ پاسخ برای کاربر ارسال شد.",
        'contact_reply_failed': "❌ ارسال پاسخ به کاربر با خطا مواجه شد.",
        'contact_reply_received': "📬 پاسخ مدیر:\n\n{message}\n\nبرای ادامه گفتگو همینجا پیام دهید.",

        # Limits
        'daily_limit_reached': "⚠️ **محدودیت ۲۴ ساعته تکمیل شد**\n\n"
                               "شما در ۲۴ ساعت گذشته {count}/{limit} اسکن انجام داده‌اید (حداکثر ۵).\n"
                               "لطفاً تا ریست شدن بازه ۲۴ ساعته صبر کنید.\n\n"
                               "در صورت نیاز با ادمین تماس بگیرید.",

        # History
        'history': "📜 **تاریخچه اسکن‌ها**\n\n{history}\n\nنمایش {count} اسکن آخر.\n⚠️ محدودیت: ۵ لینک در ۲۴ ساعت.",
        'no_history': "📭 تاریخچه‌ای ندارید.\n\nیک لینک بفرستید!",

        # Settings
        'settings': "⚙️ **تنظیمات شما**\n\n"
                    "🌐 زبان: {language}\n"
                    "🔔 اعلان‌ها: {notifications}\n"
                    "📊 محدودیت ۲۴ ساعته: {daily_limit}\n"
                    "💡 نکات: {show_tips}\n\n"
                    "⚠️ حداکثر ۵ لینک در هر ۲۴ ساعت.",

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
        'open_channel_button': "📢 ورود به کانال",
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
                       "⚠️ هر کاربر فقط می‌تواند ۵ لینک را در هر ۲۴ ساعت اسکن کند.\n\n"
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

        'limit_set': "✅ محدودیت روزانه {limit} برای کاربر {user_id} تنظیم شد (حداکثر ۵ در ۲۴ ساعت)",
        'global_limit_set': "✅ محدودیت پیش‌فرض {limit} تنظیم شد (سقف ۵ در ۲۴ ساعت)",
        'limit_reset': "✅ محدودیت به پیش‌فرض ({limit}) برگشت برای کاربر {user_id} (حداکثر ۵ در ۲۴ ساعت)",
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