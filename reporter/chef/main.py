import os
import threading
import time
from pyngrok import ngrok, conf
from telegram_bot import run_bot

def setup_ngrok():
    ngrok_token = os.environ.get('NGROK_TOKEN')
    if not ngrok_token:
        print("NGROK_TOKEN not found in environment variables. Please add it to Replit secrets.")
        return

    ngrok_config = conf.PyngrokConfig(auth_token=ngrok_token)
    conf.set_default(ngrok_config)

    try:
        public_url = ngrok.connect(5000)  # Connect to the Flask server port
        print(f' * ngrok tunnel "{public_url}" -> "http://127.0.0.1:5000"')
    except Exception as e:
        print(f"An error occurred while setting up ngrok: {str(e)}")

def run_flask_server():
    from deployment import run
    run()

def keep_polling():
    t = threading.Thread(target=run_flask_server)
    t.start()

def update_bot_status():
    from deployment import update_bot_status as update_status
    update_status()

def main():
    print("Starting main.py")

    # Start the Flask server in a separate thread
    server_thread = threading.Thread(target=keep_polling, daemon=True)
    server_thread.start()

    # Wait for the Flask server to start
    time.sleep(2)

    # Set up ngrok in a separate thread
    ngrok_thread = threading.Thread(target=setup_ngrok, daemon=True)
    ngrok_thread.start()

    print("Starting keep_polling in a separate thread")
    # This line is redundant now as we've already started the server thread
    # polling_thread = threading.Thread(target=keep_polling, daemon=True)
    # polling_thread.start()

    print("Calling run_bot()")
    run_bot(keep_polling, update_bot_status)

    # These lines will not be reached as run_bot() runs indefinitely
    # server_thread.join()
    # ngrok_thread.join()

    print("Main script execution completed")

if __name__ == "__main__":
    main()