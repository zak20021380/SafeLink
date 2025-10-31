"""
Configuration management for SafeClick bot
Loads settings from environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# Admin User IDs (comma-separated in .env)
ADMIN_IDS_STR = os.getenv('ADMIN_IDS', '')
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(',') if id.strip().isdigit()]

# Database Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/safeclick.db')

# Bot Settings
DEFAULT_DAILY_LIMIT = int(os.getenv('DEFAULT_DAILY_LIMIT', '50'))

# Validate required settings
if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    raise ValueError("❌ BOT_TOKEN not set in .env file! Get it from @BotFather")

if not ADMIN_IDS:
    print("⚠️  Warning: No ADMIN_IDS set in .env file!")
    print("   Get your ID from @userinfobot and add it to .env")

print("✅ Configuration loaded successfully")
print(f"📊 Default daily limit: {DEFAULT_DAILY_LIMIT}")
print(f"👨‍💼 Admin IDs: {ADMIN_IDS}")