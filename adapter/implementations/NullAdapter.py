from adapter.base import TerminalAdapterInterface


class NullAdapter(TerminalAdapterInterface):
    err = "This terminal emulator is not supported."

    @staticmethod
    def is_available():
        return True

    def set_image_file_path(self, image_file_path):
        print(self.err)

    def clear(self):
        print(self.err)
