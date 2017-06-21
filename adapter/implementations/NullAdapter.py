from adapter.base import TerminalAdapterInterface


class NullAdapter(TerminalAdapterInterface):
    err = "Terminal emulator not supported."

    def clear(self):
        print(self.err)

    def set_pokemon(self, pokemon):
        print(self.err)
