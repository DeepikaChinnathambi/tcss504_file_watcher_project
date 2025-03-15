import os

from watchdog.events import FileSystemEventHandler
from FileWatcherModel import FileModel
from File import FileClass
import time


class FileWatcherHandler(FileSystemEventHandler):
    """Handles file system events and notifies observers."""

    def __init__(self, model, view, allowed_extensions ):
        self.model = model
        self.view = view

        # watchdog has a weird thing where it will fire off two events for a single change...
        # to alleviate doubleing up the display with two events, we can save the prior one and compare back to see if
        # the same file/time/event is being fired off and if so then don't display it
        self.cur_time = None
        self.cur_date = None
        self.src_path = None
        self.allowed_extensions = allowed_extensions

    def _is_valid_file(self, file_path):
        """Check if the file has a valid extension."""
        _, ext = os.path.splitext(file_path)  # Extract extension
        print("is_valid_file = ", ext)
        return ext.lower() in self.allowed_extensions

    def on_any_event(self, event):
        # a dumb way to do this but if the dir, time, and date are all the same then it is likely a duplicate event
        if event.is_directory  or (event.src_path==self.src_path and self.cur_time==time.strftime("%H:%M:%S") and self.cur_date==time.strftime("%Y-%m-%d")):
            return None
        elif self._is_valid_file(event.src_path):
            # save it to the "warehouse" with event object , date and time
            self.cur_time = time.strftime("%H:%M:%S")
            self.cur_date = time.strftime("%Y-%m-%d")
            filename_with_ext = os.path.basename(event.src_path)
            filename, file_extension = os.path.splitext(filename_with_ext)

            self.model.update_file(filename, file_extension, event.event_type, self.cur_date, self.cur_time)
            self.view.display_event(filename, file_extension, event.event_type, self.cur_date, self.cur_time)
            # print("Watchdog received %s event - %s at %s on %s" % (event.event_type, event.src_path, cur_time, cur_date))

