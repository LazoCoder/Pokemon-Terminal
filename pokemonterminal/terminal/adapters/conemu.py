import os
import sys

from . import TerminalProvider as _TProv


class ConEmuProvider(_TProv):

    def is_compatible() -> bool:
        return "CONEMUPID" in os.environ

    def change_terminal(path: str):
        subprocess.run(['ConEmuC', '-GuiMacro', 'SetOption("Background Image", "{}")'.format(path)], check=True)

    def clear():
        subprocess.run(['ConEmuC', '-GuiMacro', 'SetOption("Background Image", "")'], check=True)

    def __str__():
        return "ConEmu"
