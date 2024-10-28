import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from chefwriter import AIHandler

handler = AIHandler()

print("Telegram bot script started")

# Retrieve the bot token from environment variables
TOKEN = os.environ['TELEGRAM_KEY']
print(f"Bot token retrieved: {TOKEN[:5]}...{TOKEN[-5:]}")

def split_message(message, chunk_size=300):
    # Check if message is empty or not a string
    if not isinstance(message, str) or len(message) == 0:
        return []
        
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Received /start command from user {update.effective_user.id}")
    print(f"Payload: {update.to_dict()}")
    response = 'Hello! I am your Telegram bot. How can I help you?'
    await update.message.reply_text(response)
    print(f"Sent response to user {update.effective_user.id}: {response}")


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Received /help command from user {update.effective_user.id}")
    print(f"Payload: {update.to_dict()}")
    # Prepare the prompt for the LLM
    await update.message.reply_text(response)
    print(f"Sent response to user {update.effective_user.id}: {response}")


async def handle_message(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print(f"Received message from user {update.effective_user.id}: {text}")
    print(f"Payload: {update.to_dict()}")
    prompt = f"""
    You're getting user information. 
    {text}
    """

    # Generate response using LLM
    response = handler.agentchat(prompt)

    response_chunks = split_message(response)

    print(f"DEBUG: payload from agentchat function: {response}")

    # Check if the response is empty
    if not response:
        response = "Sorry, I didn't get that. Can you please repeat?"

    # Ensure response is not empty before sending it
    # Send each chunk as a separate message
    for chunk in response_chunks:
        await update.message.reply_text(chunk)
    print(f"Sent response to user {update.effective_user.id}: {response}")


def run_bot(keep_polling, update_bot_status):
    print("Setting up the Telegram bot")

    application = Application.builder().token(TOKEN).build()
    print("Application built successfully")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Handlers added to the application")

    print("Starting bot polling")
    application.run_polling()


# No need for main() function or __main__ block in this file
