import os

from adapter.base import TerminalAdapterInterface


class Terminology(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        return os.environ.get("TERMINOLOGY") == '1'

    def set_pokemon(self, pokemon):
        os.system('tybg "{}"'.format(pokemon.get_path()))

    def clear(self):
        os.system("tybg")
