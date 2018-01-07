import os

from . import TerminalProvider as _TProv


class Terminology(_TProv):
    def is_compatible() -> bool:
        return os.environ.get("TERMINOLOGY") == '1'

    def change_terminal(path: str):
        os.system('tybg "{}"'.format(path))

    def clear():
        os.system("tybg")
