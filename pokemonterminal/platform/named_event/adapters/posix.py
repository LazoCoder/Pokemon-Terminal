import posix_ipc

from . import NamedEvent

class PosixNamedEvent(NamedEvent):
    """
    A wrapper for named events using a named semaphore
    """

    def __init__(self, name: str):
        semaphore_name = '/' + name
        try:
            self.__semaphore = posix_ipc.Semaphore(semaphore_name, flags=posix_ipc.O_CREX)
            self.__duplicate = True
        except posix_ipc.ExistentialError: # Semaphores are reconsidering their life choices
            self.__semaphore = posix_ipc.Semaphore(semaphore_name)
            self.__duplicate = False

    # NOTE this doesn't works on macOS, see http://semanchuk.com/philip/posix_ipc/#platforms
    def is_set(self) -> bool:
        return self.__semaphore.value > 0

    def set(self):
        self.__semaphore.release()

    def clear(self):
        try:
            # Decrement until we reach 0 (in which case BusyError will be thrown)
            for _ in range(self.__semaphore.value if posix_ipc.SEMAPHORE_VALUE_SUPPORTED else posix_ipc.SEMAPHORE_VALUE_MAX):
                self.__semaphore.acquire(0)
        except posix_ipc.BusyError:
            return

    def wait(self, timeout=None):
        self.__semaphore.acquire(timeout)

    def is_duplicate(self) -> bool:
        return self.__duplicate

    def name(self) -> str:
        return self.__semaphore.name

    def close(self):
        self.__semaphore.close()
