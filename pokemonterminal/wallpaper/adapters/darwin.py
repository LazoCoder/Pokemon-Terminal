from . import WallpaperProvider as _WProv
import subprocess as _sp
import sys as _sys


class DarwinProvider(_WProv):
    __osa_script_fmt = """tell application "System Events"
    \ttell current desktop
    \t\tset picture to "{}"
    \tend tell
    end tell"""

    def __run_osascript(stream):
        p = _sp.Popen(['osascript'], stdout=_sp.PIPE,
                      stdin=_sp.PIPE)
        p.stdin.write(stream)
        p.communicate()
        p.stdin.close()

    def change_wallpaper(path: str) -> None:
        script = DarwinProvider.__osa_script_fmt.format(path)
        DarwinProvider.__run_osascript(str.encode(script))

    def is_compatible() -> bool:
        return _sys.platform == "darwin"

    def __str__():
        return "MacOS Desktop Environment"
