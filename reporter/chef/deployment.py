from flask import Flask, jsonify, request
from threading import Thread, Lock
import time
from importlib import reload
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os
from datetime import datetime
import pytz

app = Flask('')

# Enhanced status tracking
status = {
    "last_update_time": None,
    "total_messages_received": 0,
    "active_modules": {},
    "last_reload_time": None,
    "uptime_start": datetime.now(pytz.timezone('America/New_York')),
}
status_lock = Lock()

class ModuleReloader(FileSystemEventHandler):
    def __init__(self, delay=20.0):  # 20 second delay
        self.delay = delay
        self.timer = None
        self.last_modified = {}
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            module_name = os.path.basename(event.src_path)[:-3]
            try:
                if module_name in sys.modules:
                    reload(sys.modules[module_name])
                    with status_lock:
                        status["last_reload_time"] = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S %Z')
                        status["active_modules"][module_name] = "reloaded"
                    print(f"Hot reloaded: {module_name}")
            except Exception as e:
                print(f"Hot reload failed for {module_name}: {str(e)}")

@app.route('/')
def home():
    return "Service is running"

@app.route('/bot_status')
def bot_status():
    with status_lock:
        return jsonify({
            "status": "alive",
            "last_update": status["last_update_time"],
            "total_messages": status["total_messages_received"],
            "uptime_since": status["uptime_start"].strftime('%Y-%m-%d %H:%M:%S %Z'),
            "last_reload": status["last_reload_time"],
            "active_modules": status["active_modules"]
        })

@app.route('/restart', methods=['POST'])
def restart_bot():
    try:
        os._exit(0)  # This will trigger Cloud Run to restart the container
        return jsonify({"status": "restarting"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/reload', methods=['POST'])
def manual_reload():
    module_name = request.json.get('module', None)
    try:
        if module_name and module_name in sys.modules:
            reload(sys.modules[module_name])
            with status_lock:
                status["last_reload_time"] = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S %Z')
                status["active_modules"][module_name] = "manually reloaded"
            return jsonify({"status": "success", "message": f"Reloaded {module_name}"})
        return jsonify({"status": "error", "message": "Module not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def setup_hot_reload():
    event_handler = ModuleReloader()
    observer = Observer()
    observer.schedule(event_handler, path='reporter/chef/', recursive=True)
    observer.start()
    print("Hot reloading enabled")

def run():
    try:
        setup_hot_reload()
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Flask app error: {str(e)}")

def keep_polling():
    t = Thread(target=run)
    t.daemon = True  # Make thread daemon so it exits when main program does
    t.start()

def update_bot_status():
    with status_lock:
        status["last_update_time"] = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S %Z')
        status["total_messages_received"] += 1

def reset_status():
    with status_lock:
        status["last_update_time"] = None
        status["total_messages_received"] = 0
        status["active_modules"] = {}
        status["last_reload_time"] = None