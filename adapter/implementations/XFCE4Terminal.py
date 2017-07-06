import os

from adapter.base import TerminalAdapterInterface

class XFCE4Terminal(TerminalAdapterInterface):
    filename = "$HOME/.config/xfce4/terminal/terminalrc"
    setting_field = "BackgroundImageFile"

    @staticmethod
    def is_available():
        return "xfce4-terminal" in os.environ.get('COLORTERM', "").lower()
        
    def set_image_file_path(self, set_image_file_path):
        command = "cat {0} | grep -v {1} > /tmp/term-cfg.temp"
        os.system(command.format(self.filename,
                                 self.setting_field))

        command = "(echo -n {1}={2}) >> /tmp/term-cfg.temp && cp /tmp/term-cfg.temp {0}"
        os.system(command.format(self.filename,
                                 self.setting_field,
                                 set_image_file_path))

    def clear(self):
        command = "cat {0} | grep -v {1} > /tmp/term-cfg.temp"
        os.system(command.format(self.filename,
                                 self.setting_field))

        command = "cp /tmp/term-cfg.temp {0}"
        os.system(command.format(self.filename))

