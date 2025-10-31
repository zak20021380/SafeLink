"""
SafeClick Bot - Startup Script
Simple runner to start the bot
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    try:
        from bot.main import main
        print("="*50)
        print("🚀 Starting SafeClick Bot...")
        print("="*50)
        print("📝 Press Ctrl+C to stop\n")
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)