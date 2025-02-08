from abc import ABC, abstractmethod

"""
Observable class to notify Observer objects of changes or updates
"""
class Observable(ABC):
    def __init__(self):
        self.observers = []
        self._status_changed = False

    #
    @abstractmethod
    def add_observer(self, observer):
        """
        add observer object to list of observables
        Args:
            observer obj
        Returns: None
        """
        self.observers.append(observer)

    @abstractmethod
    def remove_observer(self, observer):
        """
        remove observer from list of observers, I could add functionality to also erase the self._observable from the
        Observer parent class, but decided against it
        Args:
            observer:
        Returns:
            None
        """
        self.observers.remove(observer)

    #
    @abstractmethod
    def notify_observers(self, observer):
        """
        for each of the observers, trigger the update method of that class to update the observer
        Args:
            observer obj
        Returns: None
        """
        for observer in self.observers:
            observer.update()

    @abstractmethod
    def set_changed(self):
        self._status_changed = True

    @abstractmethod
    def has_changed(self,hobbit_count, dwarf_count, elf_count, human_count):
        pass

    @abstractmethod
    def clear_changed(self):
        self._status_changed = False


