from os import environ
from subprocess import run

from . import TerminalProvider as _TProv


class TilixProvider(_TProv):
    __setting_key = "com.gexperts.Tilix.Settings"
    __setting_field = "background-image"

    @staticmethod
    def is_compatible() -> bool:
        return "TILIX_ID" in environ

    @staticmethod
    def change_terminal(path: str):
        run(["gsettings", "set", TilixProvider.__setting_key, TilixProvider.__setting_field, path], check=True)

    @staticmethod
    def clear():
        run(["gsettings", "reset", TilixProvider.__setting_key, TilixProvider.__setting_field], check=True)

    def __repr__(self):
        return "Tilix"
