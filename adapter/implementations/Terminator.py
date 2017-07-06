import os

from adapter.base import TerminalAdapterInterface

class Terminator(TerminalAdapterInterface):
    filename = "$HOME/.config/terminator/config"
    setting_field = "background_image"

    @staticmethod
    def is_available():
        return "TERMINATOR_UUID" in os.environ

    def set_image_file_path(self, set_image_file_path):
        command = "sed -i 's#{1} = .*#{1} = {2}#' {0}"
        os.system(command.format(self.filename,
                                 self.setting_field,
                                 set_image_file_path))

    def clear(self):
        command = "sed -i 's#{1} = .*#{1} = #' {0}"
        os.system(command.format(self.filename,
                                 self.setting_field))
