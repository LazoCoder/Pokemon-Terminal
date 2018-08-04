import os
import sys
from pathlib import PosixPath

from . import NamedEvent


class PosixNamedEvent(NamedEvent):
    """
    A wrapper for named events using a FIFO (named pipe)
    """

    __self_references = ['self', str(os.getpid()), 'thread-self']

    @staticmethod
    def __build_fifo_path(name: str) -> PosixPath:
        return PosixPath('/') / 'run' / 'user' / str(os.getuid()) / 'pokemon-terminal' / name

    @staticmethod
    def __generate_handle_list() -> [PosixPath]:
        for p in PosixPath('/proc').glob('*/fd/*'):
            if not any(p.parts[2] == s for s in PosixNamedEvent.__self_references):
                yield p.resolve()

    @staticmethod
    def __has_open_file_handles(path: PosixPath) -> bool:
        if sys.platform != 'darwin':
            realpath = path.resolve()
            return any(realpath == p for p in PosixNamedEvent.__generate_handle_list())
        else:
            # TODO
            raise NotImplementedError("macOS doesn't have /proc")

    @staticmethod
    def exists(name: str) -> bool:
        p = PosixNamedEvent.__build_fifo_path(name)
        if not p.is_fifo():
            return False
        else:
            return PosixNamedEvent.__has_open_file_handles(p)

    def __init__(self, name: str):
        p = PosixNamedEvent.__build_fifo_path(name)
        if not p.is_fifo():
            os.makedirs(p.parent, exist_ok=True)
            os.mkfifo(p)

        self.__path = p
        self.__fifo = os.open(p, os.O_NONBLOCK)  # Keep a handle to the FIFO for exists() to detect us
        self.__fifo_in = None
        self.__fifo_out = None
        self.__name = name

    def signal(self):
        if self.__fifo_out is None:
            # This blocks until we have someone available on the other end for reading
            self.__fifo_out = os.open(self.__path, os.O_WRONLY)

        # Send out a write to every consumer (except ourself)
        while PosixNamedEvent.__has_open_file_handles(self.__path):
            os.write(self.__fifo_out, b"1")

    def wait(self):
        if self.__fifo_in is None:
            # This blocks until we have someone available on the other end for writing
            self.__fifo_in = os.open(self.__path, os.O_RDONLY)
        os.read(self.__fifo_in, 1)

    def name(self) -> str:
        return self.__name

    def close(self):
        if self.__fifo_in is not None:
            os.close(self.__fifo_in)
        if self.__fifo_out is not None:
            os.close(self.__fifo_out)
        os.close(self.__fifo)
