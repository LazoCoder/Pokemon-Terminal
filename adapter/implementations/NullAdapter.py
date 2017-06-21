from adapter.base import TerminalAdapterInterface


class NullAdapter(TerminalAdapterInterface):
    err = "This terminal emulator is not supported."

    @staticmethod
    def is_available():
        return True

    def set_pokemon(self, pokemon):
        print(self.err)

    def clear(self):
        print(self.err)
