import os

from pokemonterminal.adapter.base import TerminalAdapterInterface


class Terminology(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        return os.environ.get("TERMINOLOGY") == '1'

    def set_image_file_path(self, image_file_path):
        os.system('tybg "{}"'.format(image_file_path))

    def get_image_file_number(self):
        # TODO: Check the way to get the background image path in Terminology
        return 0

    def clear(self):
        os.system("tybg")
