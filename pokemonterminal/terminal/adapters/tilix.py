from os import environ
from subprocess import run

from . import TerminalProvider as _TProv


class TilixProvider(_TProv):
    setting_key = "com.gexperts.Tilix.Settings"
    setting_field = "background-image"

    def is_compatible() -> bool:
        return "TILIX_ID" in environ

    def change_terminal(path: str):
        command = f'gsettings set {TilixProvider.setting_key} {TilixProvider.setting_field} "{path}"'
        run(command, shell=True, check=True)

    def clear():
        command = f'gsettings reset {TilixProvider.setting_key} {TilixProvider.setting_field}'
        run(command, shell=True, check=True)

    def __str__():
        return "Tilix"
