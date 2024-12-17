import asyncio
import nest_asyncio
from flask import Flask
from telegram_bot import run_bot
from threading import Thread

# Allow nested event loops
nest_asyncio.apply()

# Flask app to keep Replit Reserved Server happy
app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=3000)  # Runs Flask on port 3000 for Replit

def main():
    try:
        # Run Flask server in a separate thread
        flask_thread = Thread(target=run_flask)
        flask_thread.start()

        # Run the Telegram bot with polling
        asyncio.run(run_bot())
    except Exception as e:
        print(f"Critical error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
