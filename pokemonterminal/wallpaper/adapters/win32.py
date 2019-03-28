import ctypes
import sys

from . import WallpaperProvider as _WProv


class Win32Provider(_WProv):
    __SPI_SETDESKWALLPAPER = 20

    def change_wallpaper(path: str):
        ctypes.windll.user32.SystemParametersInfoW(Win32Provider.__SPI_SETDESKWALLPAPER, 0, path, 0)

    def is_compatible() -> bool:
        return sys.platform == "win32"

    def __str__():
        return "Windows Desktop"
