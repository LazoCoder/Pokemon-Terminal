import os
import subprocess

from . import TerminalProvider as _TProv


class ItermProvider(_TProv):
    # OSA script that will change the terminal background image
    __osa_script_fmt = """tell application "iTerm"
    \ttell current session of current window
    \t\tset background image to "{}"
    \tend tell
    end tell"""

    @staticmethod
    def is_compatible() -> bool:
        return "ITERM_PROFILE" in os.environ

    @staticmethod
    def __run_osascript(stream):
        p = subprocess.Popen(["osascript"], stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        p.stdin.write(stream)
        p.communicate()
        p.stdin.close()

    @staticmethod
    def change_terminal(path: str):
        stdin = ItermProvider.__osa_script_fmt.format(path)
        ItermProvider.__run_osascript(str.encode(stdin))

    @staticmethod
    def clear():
        stdin = ItermProvider.__osa_script_fmt.format("")
        ItermProvider.__run_osascript(str.encode(stdin))

    def __repr__(self):
        return "iTerm 2"
