from . import WallpaperProvider as _WProv
from os import system
from pathlib import Path
from shutil import which
import subprocess


class FehProvider(_WProv):
    def change_wallpaper(path: str):
        system(f'feh --no-fehbg --bg-fill "{path}"')

    def is_compatible() -> bool:
        root_window_prop = str(subprocess.check_output('xprop -root -notype', shell=True))
        return which("feh") is not None and \
            (Path.home() / '.fehbg').is_file() and \
            any(wm_signature in root_window_prop for wm_signature in ('I3_PID', '_OPENBOX_PID'))

    def __str__():
        return "feh wallpaper tool"
