import os
import signal
import sys
from flask import Flask
from threading import Thread
import asyncio
import nest_asyncio
from telegram_bot import run_bot
from deployment import app, keep_polling, update_bot_status

# Allow nested event loops
nest_asyncio.apply()


def signal_handler(signum, frame):
    print("Received shutdown signal, cleaning up...")
    sys.exit(0)


def run_flask():
    app.run(host='0.0.0.0', port=80)


def main():
    print("Starting main.py")
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    try:
        # Run telegram bot in main thread
        asyncio.run(run_bot(keep_polling, update_bot_status))
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
