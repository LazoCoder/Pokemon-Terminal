class WallpaperProvider:
    """
    Interface representing all the different desktop environments supported
    by pokemon-terminal if you want to implement a DE, create a module in this
    folder that implements this interface, reflection will do the rest.
    """

    def change_wallpaper(path: str):
        """
        This sets the wallpaper of the corresponding D.E of this adapter.
        :param path The full path of the required pokemon image
        """
        raise NotImplementedError()

    def is_compatible() -> bool:
        """
        checks for compatibility
        :return a boolean saying whether or not the current adaptor is
        compatible with the running D.E
        """
        raise NotImplementedError()
