import asyncio
import nest_asyncio
from flask import Flask
from telegram_bot import run_bot  # Your bot script
from threading import Thread
from deployment import setup_hot_reload  # Your hot reload script
import logger

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Allow nested event loops for compatibility with Flask and asyncio
nest_asyncio.apply()

# Flask app to keep Replit Reserved Server happy
app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Bot is running!"

def run_flask():
    """Runs the Flask server."""
    app.run(host="0.0.0.0", port=3000)  # Runs Flask on port 3000 for Replit

def main():
    logger.info('main triggered')
    observer = None  # Initialize observer for hot-reloading
    try:
        # Start hot-reloading
        observer = setup_hot_reload()
        logger.info('observer started: %s', observer)

        # Run Flask server in a separate thread
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Run the Telegram bot
        asyncio.run(run_bot())
    except Exception as e:
        print(f"Critical error in main: {e}")
    finally:
        # Clean up the hot-reload observer
        if observer:
            observer.stop()
            observer.join()
            print("Hot reload observer stopped.")

if __name__ == "__main__":
    main()
