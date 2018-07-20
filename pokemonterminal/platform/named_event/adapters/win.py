import ctypes

from . import NamedEvent

class WindowsNamedEvent(NamedEvent):
    """
    Named events using the native Windows APIs
    """

    __WAIT_OBJECT_0 = 0
    __WAIT_FAILED = 0xFFFFFFFF

    __ERROR_ALREADY_EXISTS = 183

    def __raise_last_error():
        err_no = ctypes.GetLastError()
        raise WindowsError(err_no, ctypes.FormatError(err_no))

    def __init__(self, name: str):
        event = ctypes.windll.kernel32.CreateEventW(ctypes.c_void_p(), True, False, name)
        if event == 0:
            WindowsNamedEvent.__raise_last_error()

        self.__duplicate = ctypes.GetLastError() == WindowsNamedEvent.__ERROR_ALREADY_EXISTS
        self.__event = event
        self.__name = name

    def is_set(self) -> bool:
        result = ctypes.windll.kernel32.WaitForSingleObject(self.__event, 0)
        if result == WindowsNamedEvent.__WAIT_FAILED:
            WindowsNamedEvent.__raise_last_error()
        else:
            return result == WindowsNamedEvent.__WAIT_OBJECT_0

    def set(self):
        result = ctypes.windll.kernel32.SetEvent(self.__event)
        if result == 0:
            WindowsNamedEvent.__raise_last_error()

    def clear(self):
        result = ctypes.windll.kernel32.ResetEvent(self.__event)
        if result == 0:
            WindowsNamedEvent.__raise_last_error()

    def wait(self, timeout=None):
        result = ctypes.windll.kernel32.WaitForSingleObject(self.__event, 0xffffffff if timeout is None else int(timeout * 1000))
        if result == WindowsNamedEvent.__WAIT_FAILED:
            WindowsNamedEvent.__raise_last_error()

    def is_duplicate(self) -> bool:
        return self.__duplicate

    def name(self) -> str:
        return self.__name

    def close(self):
        result = ctypes.windll.kernel32.CloseHandle(self.__event)
        if result == 0:
            WindowsNamedEvent.__raise_last_error()