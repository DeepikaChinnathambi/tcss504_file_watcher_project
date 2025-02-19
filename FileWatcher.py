from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
import time
from DataWarehouse import DataWarehouse
from File import FileClass
from FileWatcherController import FileWatcherHandler
from FileWatcherDisplay import *


class WatchDogImpl(Observer):
    def __init__(self, directory_to_watch, event_handler, fw_view):
        self.watch_directory = directory_to_watch
        self.event_handler = event_handler
        self.watchdogObserver = Observer()
        self.running = False  # Flag to control the loop
        self.view = fw_view

    def watch(self):
        self.watchdogObserver.schedule(self.event_handler, self.watch_directory, recursive=True)
        self.watchdogObserver.start()
        self.view.run()
        self.running = True
        print(f"Started watching: {self.watch_directory}")
        try:
            while self.running:  # Use a flag to control the loop
                time.sleep(1)
        except KeyboardInterrupt:
            print("Received KeyboardInterrupt. Stopping watchdog...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.stop()

    def stop(self):
        """Stop watching the directory."""
        if self.running:
            self.running = False
            self.watchdogObserver.stop()
            self.watchdogObserver.join()
            print("watchdogObserver Stopped")


class FileWatcher:
    def __init__(self, directory_to_watch, fw_model, fw_view):
        self.watch_directory = directory_to_watch
        self.warehouse = DataWarehouse()
        self.view = fw_view
        self.event_handler = FileWatcherHandler(fw_model, fw_view)
        self.watchdog = None

    def start_watchdog_for_directory(self):
        print("start watchdog on ", self.watch_directory)
        watchdog = WatchDogImpl(self.watch_directory, self.event_handler,self.view)
        watchdog.watch()

    def stop_watchdog(self):
        """Stop the watchdog."""
        if self.watchdog:
            self.watchdog.stop()

# class Handler(FileSystemEventHandler):
#     def __init__(self, warehouse=None):
#         #
#         if warehouse is None:
#             self.warehouse = DataWarehouse()
#         else:
#             self.warehouse = warehouse
#
#
#     def on_any_event(self, event):
#         if event.is_directory:
#             return None
#         else:
#             # save it to the "warehouse" with event object , date and time
#             cur_time = time.strftime("%H:%M:%S")
#             cur_date = time.strftime("%Y-%m-%d")
#             file_obj = FileClass(event, cur_date, cur_time)
#             self.warehouse.push(file_obj)
#             print("Watchdog received %s event - %s at %s on %s" % (event.event_type, event.src_path, cur_time, cur_date))



# if __name__ == "__main__":
#     model = FileModel()
#     view = View()
#     watcher1 = FileWatcher(r".\test", model,view)
#     watcher2 = FileWatcher(r".\test1", model,view)

