import os

from . import TerminalProvider as _TProv


class Tilix(_TProv):
    setting_key = "com.gexperts.Tilix.Settings"
    setting_field = "background-image"

    def is_compatible() -> bool:
        return "TILIX_ID" in os.environ

    def change_terminal(self, path: str):
        command = 'gsettings set {} {} "{}"'
        os.system(command.format(self.setting_key,
                                 self.setting_field,
                                 path))

    def clear(self):
        command = 'gsettings set {} {}'
        os.system(command.format(self.setting_key,
                                 self.setting_field))
