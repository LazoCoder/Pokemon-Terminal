class TerminalAdapterInterface(object):
    @staticmethod
    def is_available():
        """
        :return: True if the environment implies we are using this terminal.
        :rtype bool
        """
        raise NotImplementedError()

    def set_pokemon(self, pokemon):
        """
        Set the background image of the terminal.
        :param pokemon: Information about a Pokémon.
        :type pokemon: dict
        """
        raise NotImplementedError()

    def clear(self):
        """
        Clear the terminal's background image.
        """
        raise NotImplementedError()
