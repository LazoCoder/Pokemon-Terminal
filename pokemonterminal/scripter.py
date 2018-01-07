# Used for creating, running and analyzing applescript and bash scripts.
import sys

from .terminal import get_current_terminal_adapters
from .wallpaper import get_current_wallpaper_adapters

TERMINAL_PROVIDER = None
WALLPAPER_PROVIDER = None


def __init_terminal_provider():
    global TERMINAL_PROVIDER
    if TERMINAL_PROVIDER is not None:
        return
    providers = get_current_terminal_adapters()
    if len(providers) > 1:
        # All this if is really not supposed to happen at all whatsoever
        # really what kind of person has 2 simultaneous T.E???
        print("Multiple providers found select the appropriate one:")
        for i, x in enumerate(providers):
            print(f'{i}. {x.__str__()}')
        print("If some of these make no sense or are irrelevant please file " +
              "an issue in https://github.com/LazoCoder/Pokemon-Terminal")
        print("=> ", end='')
        inp = None
        while inp is None:
            try:
                inp = int(input())
                if inp >= len(providers):
                    raise ValueError()
            except ValueError as _:
                print("Invalid number, try again!")
        TERMINAL_PROVIDER = providers[inp]
    elif len(providers) <= 0:
        print("Your terminal emulator isn't supported at this time.")
        sys.exit()
    else:
        TERMINAL_PROVIDER = providers[0]


def __init_wallpaper_provider():
    global WALLPAPER_PROVIDER
    if WALLPAPER_PROVIDER is not None:
        return
    providers = get_current_wallpaper_adapters()
    if len(providers) > 1:
        # All this if is really not supposed to happen at all whatsoever
        # really what kind of person has 2 simultaneous D.E???
        print("Multiple providers found select the appropriate one:")
        for i, x in enumerate(providers):
            print(f'{i}. {x.__str__()}')
        print("If some of these make no sense or are irrelevant please file " +
              "an issue in https://github.com/LazoCoder/Pokemon-Terminal")
        print("=> ", end='')
        inp = None
        while inp is None:
            try:
                inp = int(input())
                if inp >= len(providers):
                    raise ValueError()
            except ValueError as _:
                print("Invalid number, try again!")
        WALLPAPER_PROVIDER = providers[inp]
    elif len(providers) <= 0:
        print("Your desktop environment isn't supported at this time.")
        sys.exit()
    else:
        WALLPAPER_PROVIDER = providers[0]


def clear_terminal():
    __init_terminal_provider()
    TERMINAL_PROVIDER.clear()


def change_terminal(image_file_path):
    if not isinstance(image_file_path, str):
        print("A image path must be passed to the change terminal function.")
        return
    __init_terminal_provider()
    TERMINAL_PROVIDER.change_terminal(image_file_path)


def change_wallpaper(image_file_path):
    if not isinstance(image_file_path, str):
        print("A image path must be passed to the change wallpapper function.")
        return
    __init_wallpaper_provider()
    WALLPAPER_PROVIDER.change_wallpaper(image_file_path)
