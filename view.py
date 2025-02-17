class FileView:
    """Handles user interface (console output for now)."""

    @staticmethod
    def display_event(file_metadata):
        print(f"File Event: {file_metadata}")

    @staticmethod
    def display_all_files(file_store):
        print("\nCurrent Watched Files:")
        for file_metadata in file_store.values():
            print(file_metadata)
