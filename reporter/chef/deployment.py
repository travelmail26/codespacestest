
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from importlib import reload
import sys
import os

class ModuleReloader(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            module_name = os.path.basename(event.src_path)[:-3]
            try:
                if module_name in sys.modules:
                    reload(sys.modules[module_name])
                    print(f"Hot reloaded: {module_name}")
            except Exception as e:
                print(f"Hot reload failed for {module_name}: {str(e)}")

def setup_hot_reload():
    event_handler = ModuleReloader()
    observer = Observer()
    observer.schedule(event_handler, path='reporter/chef/', recursive=True)
    observer.start()
    print("Hot reloading enabled")
