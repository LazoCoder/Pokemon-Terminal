import os
import subprocess

from adapter.base import TerminalAdapterInterface

osa_script_fmt = """tell application "iTerm"
\ttell current session of current window
\t\tset background image to "{}"
\tend tell
end tell"""


class ITerm(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        return os.environ.get("ITERM_PROFILE")

    def __generate_osascript(self, path):
        # Create the content for script that will change the terminal background image.
        return osa_script_fmt.format(path)

    def __run_osascript(self, stream):
        p = subprocess.Popen(['osascript'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        p.stdin.write(stream)
        p.communicate()
        p.stdin.close()

    def set_pokemon(self, pokemon):
        stdin = self.__generate_osascript(pokemon.get_path())
        self.__run_osascript(str.encode(stdin))

    def clear(self):
        stdin = self.__generate_osascript("")
        self.__run_osascript(str.encode(stdin))
