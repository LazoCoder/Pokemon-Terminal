from . import WallpaperProvider as _WProv
from os import system
from pathlib import Path
from shutil import which

# If someone uses feh for wallpapers, there is a high probability ~/.fehbg exists, so let's base us on it.

class FehAdapter(_WProv):
    def change_wallpaper(path: str):
        system(f'feh --no-fehbg --bg-fill "{path}"')

    def is_compatible() -> bool:
        return which("feh") is not None and (Path.home() / '.fehbg').is_file()

    def __str__():
        return "feh wallpaper tool"
