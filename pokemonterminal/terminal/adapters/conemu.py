import os
import subprocess
import sys

from . import TerminalProvider as _TProv


class ConEmuProvider(_TProv):

    def is_compatible() -> bool:
        return "CONEMUPID" in os.environ

    def __run_command(command: str):
        output = subprocess.check_output(f'ConEmuC -GuiMacro {command}').decode(sys.stdout.encoding)
        if output != 'OK':
            print(output)

    def change_terminal(path: str):
        # ConEmuC supports its own character escaping, so escape the backslashes just to be sure
        ConEmuProvider.__run_command('SetOption("Background Image", "{}")'.format(path.replace("\\", "\\\\")))

    def clear():
        ConEmuProvider.__run_command('SetOption("Background Image", "")')

    def __str__():
        return "ConEmu"
