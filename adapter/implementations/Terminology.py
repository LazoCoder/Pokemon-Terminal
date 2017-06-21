import os

from adapter.base import TerminalAdapterInterface


class Terminology(TerminalAdapterInterface):
    def set_pokemon(self, pokemon):
        os.system('tybg "%s"'.format(pokemon.get_path()))

    def clear(self):
        os.system("tybg")
