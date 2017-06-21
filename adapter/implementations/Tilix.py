import os

from adapter.base import TerminalAdapterInterface


class Tilix(TerminalAdapterInterface):
    setting_key = "com.gexperts.Tilix.Settings"
    setting_field = "background-image"

    def set_pokemon(self, pokemon):
        command = 'gsettings set %s %s "%s"'
        os.system(command.format(self.setting_key,
                                 self.setting_field,
                                 pokemon.get_path()))

    def clear(self):
        command = 'gsettings set %s %s'
        os.system(command.format(self.setting_key,
                                 self.setting_field))
