import sys
from ctypes import windll

from . import WallpaperProvider as _WProv


class Win32Provider(_WProv):
    __SPI_SETDESKWALLPAPER = 20

    @staticmethod
    def change_wallpaper(path: str):
        windll.user32.SystemParametersInfoW(Win32Provider.__SPI_SETDESKWALLPAPER, 0, path, 0)

    @staticmethod
    def is_compatible() -> bool:
        return sys.platform == "win32"

    def __repr__(self):
        return "Windows Desktop"
