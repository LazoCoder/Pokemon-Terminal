#!/usr/bin/env python3
"""The main module that brings everything together."""

import os
import random
import sys
import time
from multiprocessing import Process

from . import scripter
from pokemonterminal.command_flags import parser, is_slideshow
from pokemonterminal.database import Database
from pokemonterminal.filters import Filter

PIPE_PATH = os.environ["HOME"] + "/.pokemon-terminal-pipe"
if not os.path.exists(PIPE_PATH):
    os.mkfifo(PIPE_PATH)


# noinspection PyUnusedLocal
def daemon(time_stamp, pkmn_list):
    # TODO: Implement messaging, like status and curr pokemon
    pip = open(PIPE_PATH, 'r')
    while True:
        for msg in pip:
            msg = msg.strip()
            if msg == 'quit':
                print("Stopping the slideshow")
                sys.exit(0)
        pip = open(PIPE_PATH, 'r')


def slideshow(filtered, delay, changer_func):
    pid = os.fork()
    if pid > 0:
        print("Starting slideshow with {len(filtered)}, pokemon " +
              "and a delay of {delay} minutes between pokemon")
        print("Forked process to background with pid", pid,
              "you can stop it with -c")
        os.environ["POKEMON_TERMINAL_PID"] = str(pid)
        sys.exit(0)
    p = Process(target=daemon, args=(time.time(), filtered,))
    p.daemon = True
    p.start()
    random.shuffle(filtered)
    queque = iter(filtered)
    while p.is_alive():
        next_pkmn = next(queque, None)
        if next_pkmn is None:
            random.shuffle(filtered)
            queque = iter(filtered)
            continue
        changer_func(next_pkmn.get_path())
        p.join(delay * 60)


def main(argv):
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
    if size == 1:
        print('A single pokemon matches the specified criteria: ')

    if options.dry_run:
        options.verbose = True
    if options.verbose:
        if size > Database.MAX_ID:
            print('No pokemon has been filtered...')
        else:
            # Print the list of filtered pokemon
            [
                print("#%s - %s" % (pkmn.get_id(), pkmn.get_name().title()))
                for pkmn in Filter.filtered_list
            ]
        print("Total of %d pokemon matched the filters. Chose %s" %
              (size, target.get_name().title()))

    if options.dry_run:
        print("Dry run, exiting.")
        return

    if options.clear:
        pipe_out = os.open(PIPE_PATH, os.O_WRONLY)
        os.write(pipe_out, b"quit\n")
        os.close(pipe_out)
        scripter.clear_terminal()
        return

    if is_slideshow and options.id <= 0 and size > 1:
        if options.slideshow <= 0:
            print("Time has to be greater then 0. You can use decimal values.")
            return
        target_func = scripter.change_wallpaper if options.wallpaper else \
            scripter.change_terminal
        slideshow(Filter.filtered_list, options.slideshow, target_func)
        return

    if options.wallpaper:
        scripter.change_wallpaper(target.get_path())
    else:
        scripter.change_terminal(target.get_path())


if __name__ == "__main__":
    # Entrance to the program.
    main(sys.argv[1:])
