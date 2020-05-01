import errno
import os
import psutil
import stat

from . import NamedEvent
from unittest.mock import patch
from pathlib import PosixPath


def _isfifo_strict(path):
    # https://github.com/giampaolo/psutil/blob/release-5.4.6/psutil/_common.py#L362
    try:
        st = os.stat(path)
    except OSError as err:
        if err.errno in (errno.EPERM, errno.EACCES):
            raise
        return False
    else:
        return stat.S_ISFIFO(st.st_mode)


class PosixNamedEvent(NamedEvent):
    """
    A wrapper for named events using a FIFO (named pipe)
    """

    @staticmethod
    def __build_fifo_path(name: str) -> PosixPath:
        return PosixPath(f'/tmp/{name}/{os.getuid()}')

    @staticmethod
    def __has_open_file_handles_real(path: PosixPath) -> bool:
        for proc in psutil.process_iter():
            try:
                if proc.pid != os.getpid():
                    for file in proc.open_files():
                        if PosixPath(file.path).samefile(path):
                            return True
            except psutil.Error:
                continue
        return False

    @staticmethod
    def __has_open_file_handles(path: PosixPath) -> bool:
        # HACK psutil explicitely filters out FIFOs from open_files()
        # HACK patch the function responsible of it so it does the reverse instead
        # HACK (only enumerate FIFOs in open_files)
        try:
            with patch("psutil._psplatform.isfile_strict", _isfifo_strict):
                return PosixNamedEvent.__has_open_file_handles_real(path)
        except Exception:
            # Something happened(tm), or the platform doesn't uses isfile_strict (ex: BSD).
            # Do a best effort.
            return PosixNamedEvent.__has_open_file_handles_real(path)

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
        self.__fifo = os.open(p, os.O_NONBLOCK)  # Keep a handle to the FIFO so exists() detects us
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
