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
from deployment import setup_hot_reload

# Create logs directory if it doesn't exist
# log_dir = Path('logs')
# log_dir.mkdir(exist_ok=True)

# Create log file with timestamp
# log_file = log_dir / f'bot_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

# # Basic logging setup
# logging.basicConfig(
#     level=logging.WARNING,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler(log_file),
#         logging.StreamHandler(sys.stdout)
#     ])
# logger = logging.getLogger(__name__)

# Initialize Flask app
# app = Flask(__name__)

# Get tokens from environment with validation
try:
    TOKEN = os.environ['TELEGRAM_KEY']
    if not TOKEN:
        raise ValueError("TELEGRAM_KEY is empty")
    
except KeyError:
    raise
except Exception as e:
    raise

# Initialize AI handler
try:
    handler = AIHandler()
except Exception as e:
    raise

# Dictionary to hold conversations
conversations = {}

# Telegram Bot Functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(
            'Hello! I am your AI assistant. How can I help you today?')
    except Exception as e:
        await update.message.reply_text("error in telegram start")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message_info = {
            'chat_id': update.message.chat.id,
            'user_id': update.message.from_user.id,
            'username': update.message.from_user.username,
            'first_name': update.message.from_user.first_name,
            'message_id': update.message.message_id,
            'text': update.message.text
        }
        print('DEBUG: message_info', message_info)

        with open('reporter/chef/chat_info.txt', 'w') as f:
            json.dump(message_info, f)

        if not update.message.text:
            await update.message.reply_text("I received an empty message. Please send some text!")
            return

        # Get response from handler and collect the streamed content
        response_generator = handler.agentchat(update.message.text)
        full_response = ""
        for chunk in response_generator:
            if chunk:
                full_response += chunk
                # Send chunks as they come in
                if len(chunk.strip()) > 0:
                    await update.message.reply_text(chunk)

        if not full_response:
            await update.message.reply_text("I apologize, but I couldn't generate a proper response. Please try again.")

    except Exception as e:
        print(f"Error in handle_message: {str(e)}")
        await update.message.reply_text("An error occurred while processing your message. Please try again.")
        
async def run_bot(keep_polling, update_bot_status):
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        keep_polling()  # Start the Flask server
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        raise

def send_telegram_message(text):
    """
    Sends message to Telegram, reading chat_id from file
    Args:
        text (str): Message to send
    """
    try:
        # Read chat_id from file
        chat_id_file = 'reporter/chef/chat_info.txt'
        with open(chat_id_file, 'r') as f:
            chat_info = json.load(f)
            chat_id = chat_info.get('chat_id')
            if not chat_id:
                print("No chat_id available")
                return False

        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except FileNotFoundError:
        print(f"No chat_id.txt file found at {chat_id_file}")
        return False
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return False

# Flask Routes
# @app.route('/')
# def home():
#     return "Bot is running!"

# CURRENT_CHAT_ID = None
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     try:
#         data = request.json
#         chat_id = data['message']['chat']['id']
#         message = data['message']['text']
#         global CURRENT_CHAT_ID
#         CURRENT_CHAT_ID = chat_id

#         print(f"Received message from Telegram chat ID {chat_id}: {message}")

#         # Save chat_id to file
#         # Save chat_id to file in reporter/chef directory
#         chat_id_file = 'reporter/chef/chat_id.txt'
#         with open(chat_id_file, 'w') as f:
#             f.write(str(chat_id))

        
#         if message.lower() == "restart":
#             conversations.clear()
#             return jsonify({"status": "conversations cleared"})

#         response = handler.agentchat(message)
#         result = send_telegram_message(response, chat_id)

#         return jsonify({"status": "success"})
#     except Exception as e:
#         logger.error(f"Webhook error: {str(e)}", exc_info=True)
#         return jsonify({"status": "error", "message": str(e)})

# def run_flask():
#     print (f"run_flask in telegram_bot triggered")
#     app.run(host='0.0.0.0', port=5000)

# def main():
#     print (f"Starting Flask server in main function of telegram bot")
#     try:
#         # Start Flask in a separate thread
#         flask_thread = Thread(target=run_flask)
#         flask_thread.daemon = True
#         flask_thread.start()

#         # Run Telegram bot in the main thread
#         asyncio.run(run_telegram_bot())
#     except KeyboardInterrupt:
#         logger.warning("Bot stopped by user")
#     except Exception as e:
#         logger.critical(f"Critical error in main: {str(e)}", exc_info=True)
#         raise

if __name__ == "__main__":
    main()