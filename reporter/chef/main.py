import asyncio
import nest_asyncio
from telegram_bot import run_bot

# Allow nested event loops
nest_asyncio.apply()

def main():
    try:
        # Directly run the bot locally via polling
        asyncio.run(run_bot())
    except Exception as e:
        print(f"Critical error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
