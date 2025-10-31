"""
Configuration management for SafeClick bot
Works with Railway and local development
"""

import os

# Try loading .env only for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Read from os.environ directly (Railway injects here)
BOT_TOKEN = os.environ.get('BOT_TOKEN', os.getenv('BOT_TOKEN', ''))
ADMIN_IDS_STR = os.environ.get('ADMIN_IDS', os.getenv('ADMIN_IDS', ''))
DATABASE_PATH = os.environ.get('DATABASE_PATH', os.getenv('DATABASE_PATH', 'data/safeclick.db'))
DEFAULT_DAILY_LIMIT = int(os.environ.get('DEFAULT_DAILY_LIMIT', os.getenv('DEFAULT_DAILY_LIMIT', '50')))
URLSCAN_API_KEY = os.environ.get('URLSCAN_API_KEY', os.getenv('URLSCAN_API_KEY', ''))

# Parse admin IDs
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(',') if id.strip().isdigit()]

# Validate
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set!")

if not URLSCAN_API_KEY:
    raise ValueError("❌ URLSCAN_API_KEY not set!")

print("✅ Configuration loaded")
print(f"📊 Daily limit: {DEFAULT_DAILY_LIMIT}")
print(f"👨‍💼 Admin IDs: {ADMIN_IDS}")
print(f"🔑 API Key: {URLSCAN_API_KEY[:20]}...")