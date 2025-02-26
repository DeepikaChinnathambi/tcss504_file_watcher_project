import os

from watchdog.events import FileSystemEventHandler
from FileWatcherModel import FileModel
from File import FileClass
import time


class FileWatcherHandler(FileSystemEventHandler):
    """Handles file system events and notifies observers."""

    def __init__(self, model, view, observers=None):
        self.model = model
        self.view = view
        self.observers = observers if observers else []

        # watchdog has a weird thing where it will fire off two events for a single change...
        # to alleviate doubleing up the display with two events, we can save the prior one and compare back to see if
        # the same file/time/event is being fired off and if so then don't display it
        self.cur_time = None
        self.cur_date = None
        self.src_path = None


    def notify_observers(self, file_metadata):
        """Notifies all registered observers with file metadata."""
        for observer in self.observers:
            observer.update(file_metadata)

    # def on_modified(self, event):
    #     if not event.is_directory:
    #         self.model.update_file(event.src_path, "modified")
    #         file_metadata = self.model.get_file_info(event.src_path)
    #         self.view.display_event(file_metadata)
    #         self.notify_observers(file_metadata)
    #
    # def on_created(self, event):
    #     if not event.is_directory:
    #         self.model.update_file(event.src_path, "created")
    #         file_metadata = self.model.get_file_info(event.src_path)
    #         self.view.display_event(file_metadata)
    #         self.notify_observers(file_metadata)
    #
    # def on_deleted(self, event):
    #     if not event.is_directory:
    #         self.model.update_file(event.src_path, "deleted")
    #         file_metadata = self.model.get_file_info(event.src_path)
    #         self.view.display_event(file_metadata)
    #         self.notify_observers(file_metadata)

    def on_any_event(self, event):
        # a dumb way to do this but if the dir, time, and date are all the same then it is likely a duplicate event
        if event.is_directory or (event.src_path==self.src_path and self.cur_time==time.strftime("%H:%M:%S") and self.cur_date==time.strftime("%Y-%m-%d")):
            return None
        else:
            # save it to the "warehouse" with event object , date and time
            self.cur_time = time.strftime("%H:%M:%S")
            self.cur_date = time.strftime("%Y-%m-%d")
            filename = os.path.basename(event.src_path)

            self.model.update_file(filename, event.event_type, self.cur_date, self.cur_time)
            self.view.display_event(filename, event.event_type, self.cur_date, self.cur_time)
            # print("Watchdog received %s event - %s at %s on %s" % (event.event_type, event.src_path, cur_time, cur_date))

