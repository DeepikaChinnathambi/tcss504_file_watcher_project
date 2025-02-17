import os
import time

class FileMetadata:
    """Represents metadata of a watched file."""
    def __init__(self, path, event_type):
        self.path = path
        self.event_type = event_type
        self.timestamp = time.time()
        self.size = os.path.getsize(path) if os.path.exists(path) else None

    def __repr__(self):
        return f"FileMetadata(path={self.path}, event_type={self.event_type}, timestamp={self.timestamp}, size={self.size})"

class FileModel:
    """Stores and manages file metadata."""
    def __init__(self):
        self.file_store = {}  # Dictionary to store metadata

    def update_file(self, path, event_type):
        self.file_store[path] = FileMetadata(path, event_type)

    def get_all_files(self):
        return self.file_store

    def get_file_info(self, path):
        return self.file_store.get(path, None)
