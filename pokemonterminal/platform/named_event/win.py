import ctypes

from . import NamedEvent

class WindowsNamedEvent(NamedEvent):
    """
    Named events using the native Windows APIs
    """

    __SYNCHRONIZE = 0x00100000
    __EVENT_MODIFY_STATE = 2

    __WAIT_OBJECT_0 = 0
    __WAIT_FAILED = 0xFFFFFFFF

    __ERROR_FILE_NOT_FOUND = 2

    def __raise_last_error():
        err_no = ctypes.GetLastError()
        raise WindowsError(err_no, ctypes.FormatError(err_no))

    def exists(name: str) -> bool:
        event = ctypes.windll.kernel32.OpenEventW(WindowsNamedEvent.__SYNCHRONIZE | WindowsNamedEvent.__EVENT_MODIFY_STATE, False, name)
        if event == 0:
            if ctypes.GetLastError() == WindowsNamedEvent.__ERROR_FILE_NOT_FOUND:
                return False
            else:
                WindowsNamedEvent.__raise_last_error()
        else:
            result = ctypes.windll.kernel32.CloseHandle(event)
            if result == 0:
                WindowsNamedEvent.__raise_last_error()
            return True

    def __init__(self, name: str):
        event = ctypes.windll.kernel32.CreateEventW(ctypes.c_void_p(), True, False, name)
        if event == 0:
            WindowsNamedEvent.__raise_last_error()

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

    def name(self) -> str:
        return self.__name

    def close(self):
        result = ctypes.windll.kernel32.CloseHandle(self.__event)
        if result == 0:
            WindowsNamedEvent.__raise_last_error()
