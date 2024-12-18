from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from importlib import reload
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Ensures output to console
)

class ModuleReloader(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            module_name = os.path.basename(event.src_path)[:-3]
            logging.info(f"File change detected: {event.src_path}")
            try:
                if module_name in sys.modules:
                    logging.info(f"Attempting to reload module: {module_name}")
                    reload(sys.modules[module_name])
                    logging.info(f"Successfully hot reloaded: {module_name}")
                else:
                    logging.warning(f"Module {module_name} not found in sys.modules")
            except Exception as e:
                logging.error(f"Hot reload failed for {module_name}: {str(e)}\n{traceback.format_exc()}")

def setup_hot_reload():
    """Sets up the hot reload observer."""
    logging.info("Setting up hot reload...")
    event_handler = ModuleReloader()
    observer = Observer()

    paths_to_watch = ['.', 'reporter/chef/']  # Directories to monitor
    for path in paths_to_watch:
        if os.path.exists(path):
            observer.schedule(event_handler, path=path, recursive=True)

    try:
        observer.start()
        logging.info("Hot reloading enabled")
        return observer
    except Exception as e:
        logging.error(f"Failed to start hot reload: {str(e)}")
        return None
