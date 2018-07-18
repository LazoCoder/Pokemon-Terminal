from os import environ
from subprocess import run

from . import WallpaperProvider as _WProv


class GnomeProvider(_WProv):
    def change_wallpaper(path: str) -> None:
        run(f'gsettings set org.gnome.desktop.background picture-uri "file://{path}"', shell=True, check=True)

    def is_compatible() -> bool:
        return "gnome" in environ.get("GDMSESSION").lower()

    def __str__():
        return "GNOME Shell Desktop"
