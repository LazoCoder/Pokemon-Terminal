import os
from subprocess import run

from . import TerminalProvider as _TProv


class KittyProvider(_TProv):
    def is_compatible() -> bool:
        return "KITTY_WINDOW_ID" in os.environ

    def change_terminal(path: str):
        run(["kitty", "@", "set-background-image", path])

    def clear():
        run(["kitty", "@", "set-background-image", "none"])

    def __str__():
        return "Kitty"
