from os import environ
from subprocess import run

from . import WallpaperProvider as _WProv


class GnomeProvider(_WProv):
    @staticmethod
    def change_wallpaper(path: str):
        run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{path}"], check=True)

    @staticmethod
    def is_compatible() -> bool:
        return "gnome" in environ.get("DESKTOP_SESSION", default='').lower()

    def __str__(self):
        return "GNOME Shell Desktop"
