
from DataWarehouse import DataWarehouse
from FileWatcherController import FileWatcherHandler
from FileWatcherDisplay import *
from WatchDogImpl import WatchDogImpl

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





