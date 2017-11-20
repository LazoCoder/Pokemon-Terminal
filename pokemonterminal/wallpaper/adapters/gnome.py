from . import WallpaperProvider as _WProv
import os as _os


class GnomeProvider(_WProv):
    def change_wallpaper(path: str) -> None:
        _os.system('gsettings set org.gnome.desktop.background ' +
                   f'picture-uri "file://{path}"')

    def is_compatible() -> bool:
        return (_os.environ.get("GDMSESSION") is not None and
                "gnome" in _os.environ.get("GDMSESSION").lower())

    def __str__():
        return "GNOME Shell Desktop"
