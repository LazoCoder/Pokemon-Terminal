import os
import sys
from subprocess import CalledProcessError, run

from . import TerminalProvider as _TProv

def print_kitty_error(err: CalledProcessError):
    print("Failed to set kitty background. Did you configure"
          " kitty remote control correctly? (See Readme).")
    if msg := err.stderr:
        print(f"Output from kitty: \"{msg.decode().strip()}\".")


class KittyProvider(_TProv):
    def is_compatible() -> bool:
        return "KITTY_WINDOW_ID" in os.environ

    def change_terminal(path: str):
        try:
            run(["kitty", "@", "set-background-image", path], check=True, capture_output=True)
        except CalledProcessError as err:
            print_kitty_error(err)

    def clear():
        try:
            run(["kitty", "@", "set-background-image", "none"], check=True, capture_output=True)
        except CalledProcessError as err:
            print_kitty_error(err)

    def __str__():
        return "Kitty"
