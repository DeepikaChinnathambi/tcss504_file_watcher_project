from observable import Observable


class FileClass:
    """
    simple class to store events along with date and time of change.
    Note: formatting is Y-M-D and H-M-S
    class takes in an event object (looking for obj from watchdog), a date and time in the previously noted format
    """
    def __init__(self, filename, fileextension=None, event_type=None, date=None, time=None):
        self._file_name = filename
        self._file_extension = fileextension
        self._event_type = event_type
        self._date = date
        self._time = time


    @property
    def file_name(self):
        return str(self._file_name)

    @property
    def event_type(self):
        return str(self._event_type)

    @property
    def date(self):
        return str(self._date)

    @property
    def time(self):
        return str(self._time)

    @property
    def file_extension(self):
        return str(self._file_extension)

    def __str__(self):
        #return f"FileMetadata(path={self.path}, event_type={self.event_type}, timestamp={self.timestamp}, size={self.size})"
        return f"File: {self.file_name}, File Extension: {self.file_extension}, Status: {self.event_type}, Date: {self.date}, Time: {self.time}"








