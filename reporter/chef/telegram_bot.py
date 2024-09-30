import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datatest import main

print("Telegram bot script started")

# Retrieve the bot token from environment variables
TOKEN = os.environ['TELEGRAM_KEY']
print(f"Bot token retrieved: {TOKEN[:5]}...{TOKEN[-5:]}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Received /start command from user {update.effective_user.id}")
    print(f"Payload: {update.to_dict()}")
    response = 'Hello! I am your Telegram bot. How can I help you?'
    await update.message.reply_text(response)
    print(f"Sent response to user {update.effective_user.id}: {response}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Received /help command from user {update.effective_user.id}")
    print(f"Payload: {update.to_dict()}")
    # Prepare the prompt for the LLM
    await update.message.reply_text(response)
    print(f"Sent response to user {update.effective_user.id}: {response}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print(f"Received message from user {update.effective_user.id}: {text}")
    print(f"Payload: {update.to_dict()}")
    prompt = f"""
    You're getting user information. 
    {text}
    """

    # Generate response using LLM
    response = main(prompt)
    await update.message.reply_text(response)
    print(f"Sent response to user {update.effective_user.id}: {response}")

def run_bot(keep_polling, update_bot_status):
    print("Setting up the Telegram bot")

    application = Application.builder().token(TOKEN).build()
    print("Application built successfully")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Handlers added to the application")

    print("Starting bot polling")
    application.run_polling()

# No need for main() function or __main__ block in this file