from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
import time
from DataWarehouse import DataWarehouse
from File import FileClass


class FileWatcher(Observer):
    def __init__(self, directory):
        self.observer = Observer()
        self.watch_directory = directory
        self.warehouse = DataWarehouse()

    def watch(self):
        event_handler = Handler(self.warehouse)
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()



class Handler(FileSystemEventHandler):
    def __init__(self, warehouse=None):
        #
        if warehouse is None:
            self.warehouse = DataWarehouse()
        else:
            self.warehouse = warehouse


    def on_any_event(self, event):
        if event.is_directory:
            return None
        else:
            # save it to the "warehouse" with event object , date and time
            cur_time = time.strftime("%H:%M:%S")
            cur_date = time.strftime("%Y-%m-%d")
            file_obj = FileClass(event, cur_date, cur_time)
            self.warehouse.push(file_obj)
            print("Watchdog received %s event - %s at %s on %s" % (event.event_type, event.src_path, cur_time, cur_date))



if __name__ == "__main__":
    watcher = FileWatcher(r".\test")
    watcher.watch()


