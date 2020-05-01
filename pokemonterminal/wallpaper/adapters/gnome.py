from os import environ
from subprocess import run

from . import WallpaperProvider as _WProv


class GnomeProvider(_WProv):
    __session_names = ["gnome", "ubuntu"]

    def change_wallpaper(path: str):
        run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{path}"], check=True)

    def is_compatible() -> bool:
        return environ.get("DESKTOP_SESSION", default='').lower() in __session_names

    def __str__():
        return "GNOME Shell Desktop"
