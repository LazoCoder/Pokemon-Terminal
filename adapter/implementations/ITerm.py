import os
import subprocess

from adapter.base import TerminalAdapterInterface


class ITerm(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        return os.environ.get("ITERM_PROFILE")

    def __generate_osascript(self, path):
        # Create the content for script that will change the terminal background image.
        content = "tell application \"iTerm\"\n"
        content += "\ttell current session of current window\n"
        content += "\t\tset background image to \"" + path + "\"\n"
        content += "\tend tell\n"
        content += "end tell"
        return content

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
