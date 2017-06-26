import os

from adapter.base import TerminalAdapterInterface

class Terminator(TerminalAdapterInterface):
    filename = "$HOME/.config/terminator/config"
    setting_field = "background_image"

    @staticmethod
    def is_available():
        return "TERMINATOR_UUID" in os.environ

    def set_pokemon(self, pokemon):
        command = "sed -i 's#{1} = .*#{1} = {2}#' {0}"
        os.system(command.format(self.filename,
                                 self.setting_field,
                                 pokemon.get_path()))

    def clear(self):
        command = "sed -i 's#{1} = .*#{1} = #' {0}"
        os.system(command.format(self.filename,
                                 self.setting_field))
