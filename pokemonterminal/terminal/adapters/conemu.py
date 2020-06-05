import os
import subprocess
import sys

from . import TerminalProvider as _TProv


class ConEmuProvider(_TProv):
    def is_compatible() -> bool:
        return "CONEMUPID" in os.environ

    def __run_command(command: str):
        output = subprocess.check_output(
            f"ConEmuC -GuiMacro {command}", shell=True
        ).decode(sys.stdout.encoding)
        if output != "OK":
            print(output)

    def __enable_background(state: bool):
        # https://github.com/Maximus5/ConEmu/blob/be9695f5b565c28379237a5fdea3abab7fea3e3a/src/ConEmu/resource.h#L282
        ConEmuProvider.__run_command(f'SetOption("Check", 1699, {int(state)})')

    def change_terminal(path: str):
        # ConEmuC supports its own character escaping, so escape the backslashes just to be sure
        ConEmuProvider.__run_command(
            'SetOption("Background Image", "{}")'.format(path.replace("\\", "\\\\"))
        )

        # Done after setting background image to avoid the old background flashing if it was disabled.
        ConEmuProvider.__enable_background(True)

    def clear():
        ConEmuProvider.__enable_background(False)

    def __str__():
        return "ConEmu"
