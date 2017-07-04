import os

from adapter.base import TerminalAdapterInterface


class Tilix(TerminalAdapterInterface):
    setting_key = "com.gexperts.Tilix.Settings"
    setting_field = "background-image"

    @staticmethod
    def is_available():
        return "TILIX_ID" in os.environ

    def set_image_file_path(self, image_file_path):
        command = 'gsettings set {} {} "{}"'
        os.system(command.format(self.setting_key,
                                 self.setting_field,
                                 image_file_path))

    def clear(self):
        command = 'gsettings set {} {}'
        os.system(command.format(self.setting_key,
                                 self.setting_field))
