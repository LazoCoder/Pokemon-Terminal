import os

from . import TerminalProvider as _TProv


class TilixProvider(_TProv):
    setting_key = "com.gexperts.Tilix.Settings"
    setting_field = "background-image"

    def is_compatible() -> bool:
        return "TILIX_ID" in os.environ

    def change_terminal(path: str):
        command = 'gsettings set {} {} "{}"'
        os.system(command.format(TilixProvider.setting_key,
                                 TilixProvider.setting_field,
                                 path))

    def clear():
        command = 'gsettings reset {} {}'
        os.system(command.format(TilixProvider.setting_key,
                                 TilixProvider.setting_field))

    def __str__():
        return "Tilix"
