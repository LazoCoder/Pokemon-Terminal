from . import WallpaperProvider as _WProv
import subprocess as __sp
import sys as __sys


class DarwinProvider(_WProv):
    __osa_script_fmt = """tell application "System Events"
    \ttell current desktop
    \t\tset picture to "{}"
    \tend tell
    end tell"""

    def __run_osascript(stream):
        p = __sp.Popen(['osascript'], stdout=__sp.PIPE,
                       stdin=__sp.PIPE)
        p.stdin.write(stream)
        p.communicate()
        p.stdin.close()

    def change_wallpaper(path: str) -> None:
        script = DarwinProvider.__osa_script_fmt.format(path)
        DarwinProvider.__run_osascript(str.encode(script))

    def is_compatible() -> bool:
        return __sys.platform == "darwin"

    def __str__():
        return "MacOS Desktop Environment"
