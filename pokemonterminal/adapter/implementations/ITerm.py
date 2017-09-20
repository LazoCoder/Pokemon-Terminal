import os
import subprocess

from pokemonterminal.adapter.base import TerminalAdapterInterface


# OSA script that will change the terminal background image
osa_script_fmt = """tell application "iTerm"
\ttell current session of current window
\t\tset background image to "{}"
\tend tell
end tell"""

osa_script_get = """tell application "iTerm"
\ttell current session of current window
\t\treturn background image as text
\tend tell
end tell"""


class ITerm(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        return os.environ.get("ITERM_PROFILE")

    def __run_osascript(self, stream):
        p = subprocess.Popen(['osascript'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        p.stdin.write(stream)
        path = p.communicate()
        p.stdin.close()
        return path

    def set_image_file_path(self, image_file_path):
        stdin = osa_script_fmt.format(image_file_path)
        self.__run_osascript(str.encode(stdin))

    def get_image_file_number(self):
        stdin = osa_script_get.format()
        path_tuple = self.__run_osascript(str.encode(stdin))
        path_element = str(path_tuple[0])
        # The easiest check to see if we have a Pokemon as a background is checking for the presence of '/'
        if '/' in path_element:
            return path_element.split('/')[-1].split('.')[0]
        else:
            return 0

    def clear(self):
        stdin = osa_script_fmt.format("")
        self.__run_osascript(str.encode(stdin))
