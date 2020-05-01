import subprocess
import sys
from pathlib import Path
from shutil import which

from . import WallpaperProvider as _WProv


class FehProvider(_WProv):
    __compatible_wm = ["I3_PID", "_OPENBOX_PID"]

    def change_wallpaper(path: str):
        command = ["feh", "--bg-fill", path]
        if not (Path.home() / ".fehbg").is_file():
            command.insert(1, "--no-fehbg")
        subprocess.run(command, check=True)

    def __get_root_props() -> str:
        return subprocess.check_output(["xprop", "-root", "-notype"]).decode(sys.stdout.encoding)

    def is_compatible() -> bool:
        tools_are_available = which("feh") is not None and which("xprop") is not None
        if tools_are_available:
            root_props = FehProvider.__get_root_props()
            return any(wm_signature in root_props for wm_signature in FehProvider.__compatible_wm)
        else:
            return False

    def __str__():
        return "feh wallpaper tool"
