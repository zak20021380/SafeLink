# SafeClick

SafeClick is a production-ready Telegram bot that scans URLs for phishing using the PhishTank API. The bot provides bilingual (English and Persian) responses, per-user statistics, admin broadcasting tools, and safety limits to protect your infrastructure.

## Features

- ✅ Automatic URL extraction from chat messages (up to three links per message)
- ✅ Real-time phishing checks through the PhishTank API with 24-hour caching
- ✅ SQLite database tracking users, scans, preferences, and admin settings
- ✅ Bilingual support (English and Persian/Farsi) with per-user language preferences
- ✅ Force-join support to require users to join a specific channel
- ✅ Admin utilities: global stats, broadcasts, and force-join configuration
- ✅ Daily per-user scan limits and notification preferences

## Project structure

```
SafeClick/
├── bot/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── strings.py
│   └── utils.py
├── handlers/
│   ├── admin_commands.py
│   ├── callbacks.py
│   └── user_commands.py
├── data/
├── logs/
├── requirements.txt
├── .env.example
├── run.py
└── README.md
```

- `data/` and `logs/` are created automatically at runtime.

## Getting started

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:

   Copy `.env.example` to `.env` and fill in the required values.

   ```bash
   cp .env.example .env
   ```

   | Variable | Description |
   |----------|-------------|
   | `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather |
   | `ADMIN_IDS` | Comma-separated Telegram user IDs allowed to run admin commands |
   | `PHISHTANK_API_KEY` | Optional PhishTank API key (recommended) |
   | `DATABASE_PATH` | Absolute/relative path to SQLite database file |
   | `FORCE_JOIN_EXEMPT_IDS` | Comma-separated user IDs exempt from force join |
   | `LOG_LEVEL` | Logging level (e.g., INFO, DEBUG) |
   | `DEFAULT_DAILY_LIMIT` | Default daily scan limit for users |

4. **Run the bot**:

   ```bash
   python run.py
   ```

   The bot runs asynchronously using long polling. Logs are written to `logs/safeclick.log`.

## Bot commands

### User commands

- `/start` — Welcome message, stats, and language selection
- `/help` — Usage instructions
- `/scan <url>` — Scan a specific URL
- `/stats` — Show user statistics
- `/history` — Show the last 10 scans
- `/settings` — Manage preferences via inline buttons

Any text message containing URLs will automatically trigger scans (limited to three URLs per message).

### Admin commands

- `/admin` — View global statistics and force-join status
- `/broadcast <message>` — Send a broadcast to all registered users
- `/forcejoin <channel_id> <@channel>` — Require users to join a channel
- `/disableforcejoin` — Disable the force-join requirement

## Deployment tips

- Use a process manager such as `systemd`, `pm2`, or Docker to keep the bot running.
- Make regular backups of the SQLite database located under `data/` (or at the path specified in `DATABASE_PATH`).
- Monitor `logs/safeclick.log` for error reports and API rate-limit warnings.

## License

This project is provided as-is. Customize the code to match your organization's requirements.
