import os
import subprocess
import sys

from . import TerminalProvider as _TProv


class ConEmuProvider(_TProv):

    def is_compatible() -> bool:
        return "CONEMUPID" in os.environ

    def change_terminal(path: str):
        # ConEmu has issues with the quoting when using an arg list, so use shell=True
        # ConEmu requires the image path to have escaped slashes. Enforce this by converting all slashes in the path to
        # backlashes, replace all previously doubled slashes with a single slash, then replace all single slashes with
        # double backslash
        cmd = 'ConEmuC -GuiMacro SetOption("Background Image", "{}")'.format(os.path.normpath(path).replace(
            '\\\\', '\\').replace('\\', '\\\\'))
        subprocess.run(cmd, shell=True, check=True)

    def clear():
        subprocess.run('ConEmuC -GuiMacro SetOption("Background Image", "")', shell=True, check=True)

    def __str__():
        return "ConEmu"
