import os
import subprocess

from . import TerminalProvider as _TProv


class ItermProvider(_TProv):
    # OSA script that will change the terminal background image
    __osa_script_fmt = """tell application "iTerm2"
    \ttell current session of current window
    \t\tset background image to "{}"
    \tend tell
    end tell"""

    def is_compatible() -> bool:
        return "ITERM_PROFILE" in os.environ

    def __run_osascript(stream):
        p = subprocess.Popen(
            ["osascript"], stdout=subprocess.PIPE, stdin=subprocess.PIPE
        )
        p.stdin.write(stream)
        p.communicate()
        p.stdin.close()

    def change_terminal(path: str):
        stdin = ItermProvider.__osa_script_fmt.format(path)
        ItermProvider.__run_osascript(str.encode(stdin))

    def clear():
        stdin = ItermProvider.__osa_script_fmt.format("")
        ItermProvider.__run_osascript(str.encode(stdin))

    def __str__():
        return "iTerm 2"
