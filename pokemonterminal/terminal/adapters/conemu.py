import os
import subprocess
import sys

from . import TerminalProvider as _TProv


class ConEmuProvider(_TProv):

    @staticmethod
    def is_compatible() -> bool:
        return "CONEMUPID" in os.environ

    @staticmethod
    def __run_command(command: str):
        output = subprocess.check_output(f"ConEmuC -GuiMacro {command}", shell=True).decode(sys.stdout.encoding)
        if output != 'OK':
            print(output)

    @staticmethod
    def change_terminal(path: str):
        # ConEmuC supports its own character escaping, so escape the backslashes just to be sure
        ConEmuProvider.__run_command('SetOption("Background Image", "{}")'.format(path.replace("\\", "\\\\")))

    @staticmethod
    def clear():
        ConEmuProvider.__run_command('SetOption("Background Image", "")')

    def __repr__(self):
        return "ConEmu"
