#!/usr/bin/env python3.6
"""The main module that brings everything together."""

import os
import random
import sys
from multiprocessing import Process
from pathlib import Path

from . import scripter, slideshow
from pokemonterminal.command_flags import parser, is_slideshow
from pokemonterminal.database import Database
from pokemonterminal.filters import Filter
from pokemonterminal.platform.named_event import create_named_event



def main(argv=None):
    """Entrance to the program."""
    if __name__ != "__main__":
        Filter.filtered_list = [pok for pok in Filter.POKEMON_LIST]
    # TODO Lower main() complexity with factory functions or something
    options = parser.parse_args(argv)  # Parser is imported at top of file.
    try:
        options.id = int(options.id)
    except ValueError:
        options.name = options.id.lower()
        options.id = 0
        Filter.filtered_list = [
            x for x in Filter.filtered_list if options.name == x.get_name()
        ]

    size = len(Filter.filtered_list)
    if size == 0:
        print("No pokemon matches the specified filters")
        return

    if options.id <= 0:
        # TODO this doesn't account for the current set pokemon and might try
        # TODO to set the same pokemon again (essentially not doing anything)
        target = random.choice(Filter.filtered_list)
    else:
        options.id -= 1
        if len(Filter.POKEMON_LIST) > options.id:
            if len(sys.argv) > 2:
                print("ID has been specified, ignoring all filters.")
            size = 1
            target = Filter.POKEMON_LIST[options.id]
            Filter.filtered_list = [target]
        else:
            print("Invalid id specified")
            return

    if options.verbose or options.dry_run:
        if size == 1:
            print('A single pokemon matches the specified criteria: ')
        if size > Database.MAX_ID:
            print('No pokemon has been filtered...')
        else:
            # Print the list of filtered pokemon
            [
                print(f"#{pkmn.get_id()} - {pkmn.get_name().title()}")
                for pkmn in Filter.filtered_list
            ]
        print("Total of %d pokemon matched the filters. Chose %s" %
              (size, target.get_name().title()))

    if options.dry_run:
        print("Dry run, exiting.")
        return

    e = create_named_event("Pokemon-Terminal_Wallpaper" if options.wallpaper else "Pokemon-Terminal_Terminal")
    try:
        if options.clear:
            if e.is_duplicate():
                e.set()
            scripter.clear_terminal()
            return

        if is_slideshow and options.id <= 0 and size > 1:
            if e.is_duplicate():
                print("One or more slideshows is already running.\n")
                while True:
                    print("[S]top the previous slideshow(s) / ", end='')
                    if not options.wallpaper:
                        print("[I]gnore and continue / ", end='')
                    print("[A]bort")
                    inp = input("Pick one: ").lower() # FIXME weird bug: inputting s here doesn't actually close the older process but "pokemon -c" does
                    if inp == 's':
                        e.set()
                        break
                    elif inp == 'i' and not options.wallpaper:
                        break
                    elif inp == 'a':
                        return
                    else:
                        print("Not a valid option!\n")
            if options.slideshow <= 0:
                print("Time has to be greater then 0. You can use decimal values.")
                return
            e.clear()
            target_func = scripter.change_wallpaper if options.wallpaper else scripter.change_terminal
            slideshow.start(Filter.filtered_list, options.slideshow, target_func, e.name())
    finally:
        e.close()

    if options.wallpaper:
        scripter.change_wallpaper(target.get_path())
    else:
        scripter.change_terminal(target.get_path())


if __name__ == "__main__":
    # Entrance to the program.
    main(sys.argv[1:])
