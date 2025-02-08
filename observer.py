from abc import ABC, abstractmethod

"""
Observer class to watch an Observable object and track changes/notifications
"""

class Observer(ABC):
    def __init__(self, observable, obs_id):
        self._observable = observable
        self._obs_id = obs_id
        self._observable.add_observer(self)


    @abstractmethod
    def update(self):
        """
        default to using childs method
        Returns: None
        """
        pass




