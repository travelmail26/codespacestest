from flask import Flask, jsonify
from threading import Thread, Lock
import time

app = Flask('')

# Global variables to track bot status
last_update_time = None
total_messages_received = 0
status_lock = Lock()

@app.route('/')
def home():
    return "Hello. I am alive!"

@app.route('/bot_status')
def bot_status():
    with status_lock:
        return jsonify({
            "status": "alive",
            "last_update": last_update_time,
            "total_messages_received": total_messages_received
        })

def run():
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"An error occurred while running the Flask app: {str(e)}")

def keep_polling():
    t = Thread(target=run)
    t.start()

# Function to update bot status
def update_bot_status():
    global last_update_time, total_messages_received
    with status_lock:
        last_update_time = time.strftime("%Y-%m-%d %H:%M:%S")
        total_messages_received += 1

# Optional: function to reset status (if needed)
def reset_status():
    global last_update_time, total_messages_received
    with status_lock:
        last_update_time = None
        total_messages_received = 0