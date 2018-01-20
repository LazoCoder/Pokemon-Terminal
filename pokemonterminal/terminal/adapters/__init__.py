class TerminalProvider:
    """
    Interface representing all the different terminal emulators supported
    by pokemon-terminal if you want to implement a TE, create a module in this
    folder that implements this interface, reflection will do the rest.
    """

    def change_terminal(path: str):
        """
        This sets the wallpaper of the corresponding TE of this adapter.
        :param path The full path of the required pokemon image
        """
        raise NotImplementedError()

    def is_compatible() -> bool:
        """
        checks for compatibility
        :return a boolean saying whether or not the current adaptor is
        compatible with the running TE
        """
        raise NotImplementedError()

    def clear():
        """
        Clear the terminal's background image.
        """
        raise NotImplementedError()
