# SafeClick - Phishing Link Detection Bot 🛡️

Professional Telegram bot for detecting phishing and malicious links.

## ✨ Features

- 🔍 **URL Scanning** - Check links for phishing (API ready)
- 📊 **User Statistics** - Track scans, phishing found, history
- 🌐 **Bilingual** - Full English & Persian (Farsi) support
- 👨‍💼 **Admin Panel** - Complete control over bot settings
- 📢 **Broadcast** - Send messages to all users
- 🔐 **Force Join** - Require channel membership
- 📈 **Daily Limits** - Per-user and global scan limits
- 📜 **History** - Track all scanned URLs
- ⚙️ **User Settings** - Language, notifications, preferences

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Bot

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add your bot token:
```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_IDS=your_telegram_user_id
DEFAULT_DAILY_LIMIT=50
```

**Get your Telegram User ID:** Send `/start` to [@userinfobot](https://t.me/userinfobot)

### 3. Run Bot
```bash
python run.py
```

## 📱 User Commands

- `/start` - Start bot & view your stats
- `/help` - Show help message
- `/scan <url>` - Scan a specific URL
- `/stats` - View your statistics
- `/history` - View recent scans (last 10)
- `/settings` - Change language & preferences

**Auto-scan:** Just send any message with a URL!

## 👨‍💼 Admin Commands

- `/admin` - Open admin panel with statistics
- `/broadcast <message>` - Send message to all users
- `/forcejoin <channel_id> <@username>` - Enable force join
- `/disableforcejoin` - Disable force join
- `/setlimit <user_id> <limit>` - Set custom limit for user
- `/setgloballimit <limit>` - Set default limit for all
- `/userinfo <user_id>` - View user information
- `/resetlimit <user_id>` - Reset user's limit

**Examples:**
```bash
/broadcast Hello everyone! Bot updated.
/forcejoin -1001234567890 @YourChannel
/setlimit 123456789 100
/setgloballimit 50
```

## 🗄️ Database

SQLite database with 4 tables:
- **users** - User stats and activity
- **scan_history** - All scanned URLs
- **user_preferences** - Language, limits, settings
- **admin_settings** - Force join, global limits

Location: `data/safeclick.db`

## 🔌 API Integration

The bot uses a **placeholder** for URL checking. To add real phishing detection:

1. **Choose an API:**
   - PhishTank (free)
   - VirusTotal (free tier)
   - Google Safe Browsing
   - URLScan.io
   - Custom solution

2. **Edit `bot/utils.py`:**
   Replace the `check_url()` function with your API logic.

3. **Add API key to `.env`** if needed.

## 🚀 Deployment

### Local / VPS
```bash
# Run with screen
screen -S safeclick
python run.py
# Detach: Ctrl+A then D
```

### systemd Service

Create `/etc/systemd/system/safeclick.service`:
```ini
[Unit]
Description=SafeClick Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/SafeClick
ExecStart=/usr/bin/python3 run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable safeclick
sudo systemctl start safeclick
sudo systemctl status safeclick
```

## 📂 Project Structure
```
SafeClick/
├── bot/
│   ├── __init__.py         # Package init
│   ├── config.py           # Configuration
│   ├── database.py         # SQLite database
│   ├── strings.py          # Bilingual texts
│   ├── utils.py            # Helper functions
│   └── main.py             # Main bot logic
├── handlers/
│   ├── __init__.py         # Package init
│   ├── user_commands.py    # User commands
│   ├── admin_commands.py   # Admin commands
│   └── callbacks.py        # Button callbacks
├── data/                   # Database folder
├── logs/                   # Log files
├── .env                    # Your secrets
├── .gitignore             # Git ignore
├── requirements.txt        # Dependencies
├── README.md              # This file
└── run.py                 # Startup script
```

## 🐛 Troubleshooting

**Error: "BOT_TOKEN not set"**
- Create `.env` file from `.env.example`
- Add your token from @BotFather

**Error: "Module not found"**
- Run: `pip install -r requirements.txt`

**Database errors**
- Normal on first run
- Database created automatically in `data/`

## 📝 License

MIT License - Do whatever you want!

## 🤝 Contributing

Pull requests welcome!

---

**Made with ❤️ for secure browsing**