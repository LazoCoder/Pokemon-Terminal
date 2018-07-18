import subprocess
import sys
from pathlib import Path
from shutil import which

from . import WallpaperProvider as _WProv


class FehProvider(_WProv):
    compatible_wm = ('I3_PID', '_OPENBOX_PID')

    def change_wallpaper(path: str):
        if (Path.home() / '.fehbg').is_file():
            command = f'feh --bg-fill "{path}"'
        else:
            command = f'feh --no-fehbg --bg-fill "{path}"'
        subprocess.run(command, shell=True, check=True)

    def __get_root_props() -> str:
        return subprocess.check_output('xprop -root -notype', shell=True).decode(sys.stdout.encoding)

    def is_compatible() -> bool:
        return which("feh") is not None and which("xprop") is not None and \
            any(wm_signature in FehProvider.__get_root_props() for wm_signature in FehProvider.compatible_wm)

    def __str__():
        return "feh wallpaper tool"
