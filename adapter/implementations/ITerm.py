import os
import subprocess

from adapter.base import TerminalAdapterInterface

# OSA script that will change the terminal background image
osa_script_fmt = """tell application "iTerm"
\ttell current session of current window
\t\tset background image to "{}"
\tend tell
end tell"""


class ITerm(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        return os.environ.get("ITERM_PROFILE")

    def __run_osascript(self, stream):
        p = subprocess.Popen(['osascript'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        p.stdin.write(stream)
        p.communicate()
        p.stdin.close()

    def set_image_file_path(self, image_file_path):
        stdin = osa_script_fmt.format(image_file_path)
        self.__run_osascript(str.encode(stdin))

    def clear(self):
        stdin = osa_script_fmt.format("")
        self.__run_osascript(str.encode(stdin))
