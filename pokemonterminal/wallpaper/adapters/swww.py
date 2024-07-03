from subprocess import run
from shutil import which
from . import WallpaperProvider as _WProv


class SwwwProvider(_WProv):
    def change_wallpaper(path: str):
        run(["swww", "img", path], check=True)
        
    def is_compatible() -> bool:
        # check if swww is installed
        if not which("swww"):
            return False

        # check if it's working (i.e. the daemon is running)
        if run(["swww", "query"], capture_output=True).returncode != 0:
            return False

        return True

    def __str__():
        return "swww"
