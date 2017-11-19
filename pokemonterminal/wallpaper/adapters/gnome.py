from . import WallpaperProvider as __WProv
import os as __os


class GnomeProvider(__WProv):
    def change_wallpaper(path: str) -> None:
        __os.system('gsettings set org.gnome.desktop.background ' +
                    f'picture-uri "file://{path}"')

    def is_compatible() -> bool:
        return "gnome" in __os.environ.get("GDMSESSION")

    def __str__():
        return "GNOME Shell Desktop"
