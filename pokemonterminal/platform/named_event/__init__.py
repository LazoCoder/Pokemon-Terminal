from abc import ABC, abstractmethod

class NamedEvent(ABC):
    """
    Interface representing an operating system event object with a name.
    """

    @staticmethod
    @abstractmethod
    def exists(name: str) -> bool:
        """
        check if event exists
        does not returns event, use the constructor for that.
        :return a boolean indicating wether the event exists.
        """
        pass

    @abstractmethod
    def is_set(self) -> bool:
        """
        check if event set
        :return a boolean indicating wether the event has been set.
        """
        pass

    @abstractmethod
    def set(self):
        """
        sets the event
        """
        pass

    @abstractmethod
    def clear(self):
        """
        resets the event
        """
        pass

    @abstractmethod
    def wait(self, timeout=None):
        """
        block until event is set
        :param timeout Optional timeout for wait in seconds.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """
        gets the name set at creation of the event
        :return Name of the event
        """
        pass

    @abstractmethod
    def close(self):
        """
        release native resources
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
