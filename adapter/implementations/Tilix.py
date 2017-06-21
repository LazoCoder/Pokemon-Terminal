import os

from adapter.base import TerminalAdapterInterface


class Tilix(TerminalAdapterInterface):
    setting_key = "com.gexperts.Tilix.Settings"
    setting_field = "background-image"

    @staticmethod
    def is_available():
        return "TILIX_ID" in os.environ

    def set_pokemon(self, pokemon):
        command = 'gsettings set {} {} "{}"'
        os.system(command.format(self.setting_key,
                                 self.setting_field,
                                 pokemon.get_path()))

    def clear(self):
        command = 'gsettings set {} {}'
        os.system(command.format(self.setting_key,
                                 self.setting_field))
