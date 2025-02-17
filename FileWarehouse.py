class FileWarehouse(Observer):
    """Acts as an Observer that stores file metadata upon updates."""

    def __init__(self):
        self.file_records = {}

    def update(self, file_metadata):
        """Updates warehouse with file metadata."""
        self.file_records[file_metadata.path] = file_metadata
        print(f"Warehouse Updated: {file_metadata}")

    def get_all_files(self):
        """Retrieve all stored file records."""
        return self.file_records
