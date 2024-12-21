import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class JsonFileHandler(FileSystemEventHandler):
    def __init__(self, target_file):
        self.target_file = target_file
        self.file_found = False

    def on_created(self, event):
        if not self.file_found and event.src_path.endswith(self.target_file):
            self.file_found = True

def monitor_directory(directory, json_filename):    
    event_handler = JsonFileHandler(json_filename)
    
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    
    while not event_handler.file_found:
        time.sleep(60 * 5) # Monitor the directory from 5 to 5 minutes.
    
    observer.stop()
    observer.join()
