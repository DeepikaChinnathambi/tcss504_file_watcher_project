from observable import Observable


class FileClass:
    """
    simple class to store events along with date and time of change.
    Note: formatting is Y-M-D and H-M-S
    class takes in an event object (looking for obj from watchdog), a date and time in the previously noted format
    """
    def __init__(self, path, event_type=None, date=None, time=None):
        self.path = path
        self.event_type = event_type
        self._date = date
        self._time = time

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time

    def __str__(self):
        #return f"FileMetadata(path={self.path}, event_type={self.event_type}, timestamp={self.timestamp}, size={self.size})"
        return f"File: {self.path}, Status: {self.event_type}, Time: {self.time}"








