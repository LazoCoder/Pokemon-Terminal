from . import WallpaperProvider as _WProv
from os import environ as _environ, system as _system
from shutil import which as _which
from sys import exit as _exit


class I3wmAdapter(_WProv):
    def change_wallpaper(path: str):
        file = _which("feh")
        if file is None:
            # I did the checking here not to seem we don't support i3
            print("feh not found, you need it to set the background in i3.")
            _exit(0)
        _system(f'feh --bg-fill "{path}"')

    def is_compatible() -> bool:
        return 'i3' in _environ.get('XDG_CURRENT_DESKTOP', '') and \
            'i3' in _environ.get('XDG_SESSION_DESKTOP', '')
