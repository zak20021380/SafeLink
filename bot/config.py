"""
Configuration management for SafeClick bot
Loads settings from environment variables (works locally and on Railway)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# Admin User IDs (comma-separated)
ADMIN_IDS_STR = os.getenv('ADMIN_IDS', '')
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(',') if id.strip().isdigit()]

# Database Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/safeclick.db')

# Bot Settings
DEFAULT_DAILY_LIMIT = int(os.getenv('DEFAULT_DAILY_LIMIT', '50'))

# URLScan.io API Key
URLSCAN_API_KEY = os.getenv('URLSCAN_API_KEY', '')

# Validate required settings
if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    raise ValueError("❌ BOT_TOKEN not set! Add it to environment variables or .env file")

if not URLSCAN_API_KEY:
    raise ValueError("❌ URLSCAN_API_KEY not set! Add it to environment variables or .env file")

if not ADMIN_IDS:
    print("⚠️  Warning: No ADMIN_IDS set!")
    print("   Get your ID from @userinfobot and add it to environment variables")

print("✅ Configuration loaded successfully")
print(f"📊 Default daily limit: {DEFAULT_DAILY_LIMIT}")
print(f"👨‍💼 Admin IDs: {ADMIN_IDS}")
print(f"🔑 URLScan API Key: {URLSCAN_API_KEY[:20]}..." if URLSCAN_API_KEY else "🔑 No API Key")