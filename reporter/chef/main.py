
import os
import asyncio
import nest_asyncio
from telegram_bot import run_bot
from deployment import keep_polling, update_bot_status

# Allow nested event loops
nest_asyncio.apply()

def main():
    try:
        # Run the bot with the Flask server
        asyncio.run(run_bot(keep_polling, update_bot_status))
    except Exception as e:
        print(f"Critical error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
