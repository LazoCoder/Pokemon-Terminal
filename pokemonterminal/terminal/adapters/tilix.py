from os import environ
from subprocess import run

from . import TerminalProvider as _TProv


class TilixProvider(_TProv):
    __setting_key = "com.gexperts.Tilix.Settings"
    __setting_field = "background-image"

    def is_compatible() -> bool:
        return "TILIX_ID" in environ

    def change_terminal(path: str):
        run(
            [
                "gsettings",
                "set",
                TilixProvider.__setting_key,
                TilixProvider.__setting_field,
                path,
            ],
            check=True,
        )

    def clear():
        run(
            [
                "gsettings",
                "reset",
                TilixProvider.__setting_key,
                TilixProvider.__setting_field,
            ],
            check=True,
        )

    def __str__():
        return "Tilix"
