class TerminalAdapterInterface(object):
    @staticmethod
    def is_available():
        """
        :return: True if the environment implies we are using this terminal.
        :rtype bool
        """
        raise NotImplementedError()

    def set_image_file_path(self, image_file_path):
        """
        Set the background image of the terminal.
        :param image_file_path: Path to an image file.
        :rtype str
        """
        raise NotImplementedError()

    def get_image_file_number(self):
        """
        Get the number of the background image of the terminal.
        :rtype str
        """
        raise NotImplementedError()

    def clear(self):
        """
        Clear the terminal's background image.
        """
        raise NotImplementedError()
