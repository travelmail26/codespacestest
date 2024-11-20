import os
import signal
import sys
from flask import Flask
from threading import Thread
import asyncio
import nest_asyncio
from telegram_bot import run_bot
from deployment import app, keep_polling, update_bot_status
import logging
from datetime import datetime
import pytz
from alarm import check_alarms

# Setup logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.StreamHandler(sys.stdout),
#         logging.FileHandler('app.log')
#     ]
# )
# logger = logging.getLogger(__name__)

# # Allow nested event loops
nest_asyncio.apply()

# def signal_handler(signum, frame):
#     logger.warning("Received shutdown signal, cleaning up...")
#     sys.exit(0)

# def run_flask():
#     logger.info("Starting Flask server on port 80...")
#     app.run(host='0.0.0.0', port=80)

def main():
    # logger.info("=== Starting main.py ===")
    # logger.info(f"Current working directory: {os.getcwd()}")
    # logger.info(f"Environment: {os.environ.get('ENVIRONMENT', 'not set')}")

    # signal.signal(signal.SIGTERM, signal_handler)
    # signal.signal(signal.SIGINT, signal_handler)

    # # Start Flask in a separate thread
    # logger.info("Initializing Flask thread...")
    # flask_thread = Thread(target=run_flask, daemon=True)
    # flask_thread.start()

    # Start alarm checker in a separate thread
    #logger.info("Initializing alarm checker thread...")
    alarm_thread = Thread(target=check_alarms, daemon=True)
    alarm_thread.start()

    try:
        #logger.info("Attempting to start Telegram bot...")
        asyncio.run(run_bot(keep_polling, update_bot_status))
    except Exception as e:
        #logger.error(f"Critical error in main: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()