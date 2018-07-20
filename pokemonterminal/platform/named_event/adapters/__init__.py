class NamedEvent:
    """
    Interface representing an operating system event object with a name.
    """

    def __init__(self, name: str):
        """
        create NamedEvent object
        :param name Name of the event
        """
        raise NotImplementedError()

    def is_set(self) -> bool:
        """
        check if event set
        :return a boolean indicating wether the event has been set.
        """
        raise NotImplementedError()

    def set(self):
        """
        sets the event
        """
        raise NotImplementedError()

    def clear(self):
        """
        resets the event
        """
        raise NotImplementedError()

    def wait(self, timeout=None):
        """
        block until event is set
        :param timeout Optional timeout for wait in seconds.
        """
        raise NotImplementedError()

    def is_duplicate(self) -> bool:
        """
        determines if the event was created or opened as a result of creating this class
        :return True if it was opened. False if it was created.
        """
        raise NotImplementedError()

    def name(self) -> str:
        """
        gets the name set at creation of the event
        :return Name of the event
        """
        raise NotImplementedError()

    def close(self):
        """
        release native resources
        """
        raise NotImplementedError()