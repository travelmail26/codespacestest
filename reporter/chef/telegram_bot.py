from flask import Flask, request, jsonify
import requests
import json
import os
import logging
import sys
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from chefwriter import AIHandler
from threading import Thread
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# Create log file with timestamp
log_file = log_dir / f'bot_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

# Basic logging setup
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ])
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Get tokens from environment with validation
try:
    TOKEN = os.environ['TELEGRAM_KEY']
    if not TOKEN:
        raise ValueError("TELEGRAM_KEY is empty")
    logger.warning(f"Telegram token validated")
except KeyError:
    logger.critical("TELEGRAM_KEY not found in environment variables!")
    raise
except Exception as e:
    logger.critical(f"Token validation error: {str(e)}")
    raise

# Initialize AI handler
try:
    handler = AIHandler()
except Exception as e:
    logger.critical(f"Failed to initialize AIHandler: {str(e)}", exc_info=True)
    raise

# Dictionary to hold conversations
conversations = {}

# Telegram Bot Functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(
            'Hello! I am your AI assistant. How can I help you today?')
    except Exception as e:
        logger.error(f"Start command failed: {str(e)}", exc_info=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not update.message.text:
            await update.message.reply_text("I received an empty message. Please send some text!")
            return

        response = handler.agentchat(update.message.text)

        # Handle empty response from agentchat
        if not response or response.strip() == "":
            await update.message.reply_text("I apologize, but I couldn't generate a proper response. Please try again.")
            return

        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Message handling failed: {str(e)}", exc_info=True)
        await update.message.reply_text("An error occurred while processing your message. Please try again.")

async def run_telegram_bot():
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        await application.run_polling()
    except Exception as e:
        logger.critical(f"Failed to start Telegram bot: {str(e)}", exc_info=True)
        raise

async def run_bot(keep_polling, update_bot_status):
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        keep_polling()  # Start the Flask server
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.critical(f"Bot runtime error: {str(e)}", exc_info=True)
        raise

def send_telegram_message(text, chat_id):
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to send message to Telegram: {str(e)}", exc_info=True)
        raise

# Flask Routes
@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        chat_id = data['message']['chat']['id']
        message = data['message']['text']

        if message.lower() == "restart":
            conversations.clear()
            return jsonify({"status": "conversations cleared"})

        response = handler.agentchat(message)
        result = send_telegram_message(response, chat_id)

        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)})

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def main():
    try:
        # Start Flask in a separate thread
        flask_thread = Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()

        # Run Telegram bot in the main thread
        asyncio.run(run_telegram_bot())
    except KeyboardInterrupt:
        logger.warning("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Critical error in main: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()