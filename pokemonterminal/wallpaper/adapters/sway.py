from os import environ
from subprocess import run
from . import WallpaperProvider as _WProv


class SwayProvider(_WProv):
    def change_wallpaper(path: str):
        run(["swaymsg", f"output * background {path} fill"], check=True)
        
    def is_compatible() -> bool:
        return "sway" in environ.get("DESKTOP_SESSION", default='').lower()

    def __str__():
        return "sway"
