import os

from adapter.base import TerminalAdapterInterface


class Terminology(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        return os.environ.get("TERMINOLOGY") == '1'

    def set_image_file_path(self, image_file_path):
        os.system('tybg "{}"'.format(image_file_path))

    def clear(self):
        os.system("tybg")
