
from flask import Flask, request, jsonify
import requests
import json
##initialize curl
#curl -F "url=https://travelmail26-stunning-rotary-phone-qwwpw55jrf45pp-5000.app.github.dev/webhook" https://api.telegram.org/bot6413015540:AAGRAlAd6UScVAgDoP11uH4yxx8eJkzgiTw/setWebhook


app = Flask(__name__)

# Your OpenAI API key and Telegram Bot Token
API_KEY = ''
BOT_TOKEN = ''

# Dictionary to hold conversations
conversations = {}


intructionset = """your job is help me probe my emotional state. You will  do this in sequence. 
First, i need you to ask probing questions about how my emotions feel in my body and what
I think they are trying to tell me. You will always ask in a conversational style. You can may
summarize my answers and then ask one question and only one question at a time. You will not offer
solutions. You will just act curious about my emotional state and how the physical sensations in my 
body show up as different emotions. The goal of the first part is simply to help you understand
how I feel.

Second, once i give you permission, move on to the second sequence of questions which is helping me
imagine what needs to happen in my life to ease my emotions or make me feel better. You will ask 
questions that help me probe and imagine different scenrios in my life and see if they reduces
negative emotions. You will keep summarizing my responses and asking appropriate follow up questions. 
You will not propose soltuions. Your responses will be brief and conversational"""

# Function to get response from OpenAI's GPT-3
def openAI(chat_id, prompt):
    # Initialize conversation if not already done
    if chat_id not in conversations:
        conversations[chat_id] = [{"role": "system", "content": "You are a helpful friend."},
                                  {"role": "system", "content": intructionset}]
    
    # Add the user's message to the conversation
    conversations[chat_id].append({"role": "user", "content": prompt})
    
    # Make the API call
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'model': 'gpt-3.5-turbo', 'messages': conversations[chat_id]},
        timeout=30
    )
    
    result = response.json()
    
    try:
        bot_response = result['choices'][0]['message']['content']
        # Add the bot's response to the conversation
        conversations[chat_id].append({"role": "assistant", "content": bot_response})
        return bot_response
    except KeyError:
        print("Error: 'choices' key not found in API response.")
        return "An error occurred."

# Function to send a message to a Telegram chat
def telegram_bot_sendtext(bot_message, chat_id):
    data = {'chat_id': chat_id, 'text': bot_message}
    response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json=data)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    message = data['message']['text']

    if message.lower() == "restart":
        clearconversation()
        telegram_bot_sendtext("All conversations restarted.", chat_id)
        return jsonify(status="success")  # Return early after clearing conversations



    # Print the incoming message
    print(f"Incoming message from chat_id {chat_id}: {message}")

    # Generate a response using OpenAI's GPT-3
    bot_response = openAI(chat_id, message)

    # Send the response back to the Telegram chat
    telegram_bot_sendtext(bot_response, chat_id)

    return jsonify(status="success")


def clearconversation():
    # Check for the "restart" command
    
    conversations.clear()
    print("All conversations have been restarted.")

if __name__ == '__main__':
    app.run(port=5000)
