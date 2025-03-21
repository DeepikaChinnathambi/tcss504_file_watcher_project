
from DataWarehouse import DataWarehouse
from FileWatcherController import FileWatcherController
from FileWatcherDisplay import *
from WatchDogImpl import WatchDogImpl

class FileWatcher:
    def __init__(self, directory_to_watch, fw_model, fw_view, allowed_exts):
        self._watch_directory = directory_to_watch
        self._warehouse = DataWarehouse()
        self._view = fw_view
        self._event_handler = FileWatcherController(fw_model, fw_view, allowed_exts)
        self._watchdog = None

    def start_watchdog_for_directory(self):
        print("start watchdog on ", self._watch_directory)
        self._watchdog = WatchDogImpl(self._watch_directory, self._event_handler, self._view)
        self._watchdog.watch()


    def stop_watchdog(self):
        """Stop the watchdog."""
        if self._watchdog:
            self._watchdog.stop()





