"""
Configuration management for SafeClick bot
DEBUG VERSION - Shows all environment variables
"""

import os
import sys

# Try loading .env only for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

print("=" * 50)
print("🔍 DEBUGGING ENVIRONMENT VARIABLES")
print("=" * 50)

# Print ALL environment variables
print("\n📋 ALL ENVIRONMENT VARIABLES:")
for key, value in os.environ.items():
    if any(x in key.upper() for x in ['BOT', 'TOKEN', 'ADMIN', 'API', 'DAILY', 'DATABASE']):
        print(f"   {key} = {value[:20]}..." if len(value) > 20 else f"   {key} = {value}")

print("\n" + "=" * 50)

# Read variables
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
ADMIN_IDS_STR = os.environ.get('ADMIN_IDS', '')
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'data/safeclick.db')
DEFAULT_DAILY_LIMIT = int(os.environ.get('DEFAULT_DAILY_LIMIT', '50'))
URLSCAN_API_KEY = os.environ.get('URLSCAN_API_KEY', '')

# Parse admin IDs
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(',') if id.strip().isdigit()]

# Show what we got
print(f"\n✅ BOT_TOKEN: {'FOUND' if BOT_TOKEN else '❌ MISSING'}")
print(f"✅ ADMIN_IDS: {ADMIN_IDS if ADMIN_IDS else '❌ MISSING'}")
print(f"✅ URLSCAN_API_KEY: {'FOUND' if URLSCAN_API_KEY else '❌ MISSING'}")
print(f"✅ DEFAULT_DAILY_LIMIT: {DEFAULT_DAILY_LIMIT}")
print(f"✅ DATABASE_PATH: {DATABASE_PATH}")
print("=" * 50 + "\n")

# Validate
if not BOT_TOKEN:
    print("❌ BOT_TOKEN is empty!")
    print("🔍 Available env vars:", list(os.environ.keys())[:10])
    sys.exit(1)

if not URLSCAN_API_KEY:
    print("❌ URLSCAN_API_KEY is empty!")
    sys.exit(1)

print("✅ All variables loaded successfully!\n")