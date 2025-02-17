from observable import Observable


class FileClass:
    """
    simple class to store events along with date and time of change.
    Note: formatting is Y-M-D and H-M-S
    class takes in an event object (looking for obj from watchdog), a date and time in the previously noted format
    """
    def __init__(self, event_obj=None, date=None, time=None):
        self.event_obj = event_obj
        self._date = date
        self._time = time

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time








