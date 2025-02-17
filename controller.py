from watchdog.events import FileSystemEventHandler
from model import FileModel
from view import FileView


class FileWatcherHandler(FileSystemEventHandler):
    """Handles file system events and notifies observers."""

    def __init__(self, model, view, observers=None):
        self.model = model
        self.view = view
        self.observers = observers if observers else []

    def notify_observers(self, file_metadata):
        """Notifies all registered observers with file metadata."""
        for observer in self.observers:
            observer.update(file_metadata)

    def on_modified(self, event):
        if not event.is_directory:
            self.model.update_file(event.src_path, "modified")
            file_metadata = self.model.get_file_info(event.src_path)
            self.view.display_event(file_metadata)
            self.notify_observers(file_metadata)

    def on_created(self, event):
        if not event.is_directory:
            self.model.update_file(event.src_path, "created")
            file_metadata = self.model.get_file_info(event.src_path)
            self.view.display_event(file_metadata)
            self.notify_observers(file_metadata)

    def on_deleted(self, event):
        if not event.is_directory:
            self.model.update_file(event.src_path, "deleted")
            file_metadata = self.model.get_file_info(event.src_path)
            self.view.display_event(file_metadata)
            self.notify_observers(file_metadata)
