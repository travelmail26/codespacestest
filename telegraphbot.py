from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Your OpenAI API key and Telegram Bot Token
API_KEY = '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'
BOT_TOKEN = '6413015540:AAGRAlAd6UScVAgDoP11uH4yxx8eJkzgiTw'

# Function to get response from OpenAI's GPT-3
def openAI(prompt):
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'model': 'gpt-3.5-turbo', 'messages': [{"role": "user", "content": prompt}]},
        timeout=10
    )
    result = response.json()
    return result['choices'][0]['message']['content']

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

    # Generate a response using OpenAI's GPT-3
    bot_response = openAI(message)

    # Send the response back to the Telegram chat
    telegram_bot_sendtext(bot_response, chat_id)

    return jsonify(status="success")

if __name__ == '__main__':
    app.run(port=5000)


#curl -F "url=https://travelmail26-stunning-rotary-phone-qwwpw55jrf45pp-5000.app.github.dev/webhook" https://api.telegram.org/bot6413015540:AAGRAlAd6UScVAgDoP11uH4yxx8eJkzgiTw/setWebhook
