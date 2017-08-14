#!/usr/bin/env python3
"""The main module that brings everything together."""

import argparse
import os
import random
import sys
import time
from multiprocessing import Process

import filters
import scripter
from database import Database
from filters import Filter

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
        print(f"Starting slideshow with {len(filtered)}, pokemon " +
              f"and a delay of {delay} minutes between pokemon")
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
    parser = argparse.ArgumentParser(
        description='Set a pokemon to the current terminal background or '
                    'wallpaper',
        epilog='Not setting any filters will get a completely random pokemon')
    filters_group = parser.add_argument_group(
        'Filters', 'Arguments used to filter the list of pokemons with '
                   'various conditions')
    filters_group.add_argument(
        '-n',
        '--name',
        help='Filter by pokemon which name contains NAME',
        action=filters.NameFilter,
        type=str.lower)
    filters_group.add_argument(
        '-r',
        '--region',
        help='Filter the pokemons by region',
        action=filters.RegionFilter,
        choices=Database.REGIONS,
        type=str.lower)
    filters_group.add_argument(
        '-l',
        '--light',
        help='Filter out the pokemons darker then 0.xx',
        default=0.7,
        const=0.7,
        metavar='0.xx',
        nargs='?',
        type=float,
        action=filters.LightFilter)
    filters_group.add_argument(
        '-d',
        '--dark',
        help='Filter out the pokemons lighter then 0.xx',
        default=0.42,
        const=0.42,
        metavar='0.xx',
        nargs='?',
        type=float,
        action=filters.DarkFilter)
    filters_group.add_argument(
        '-t',
        '--type',
        help='Filter the pokemons by type.',
        action=filters.TypeFilter,
        choices=Database.POKEMON_TYPES,
        type=str.lower)
    filters_group.add_argument(
        '-ne',
        '--no-extras',
        help='Excludes extra pokemons',
        nargs=0,
        action=filters.NonExtrasFilter)
    filters_group.add_argument(
        '-e',
        '--extras',
        help='Excludes all non-extra pokemons',
        nargs=0,
        action=filters.ExtrasFilter)

    misc_group = parser.add_argument_group("Misc")
    misc_group.add_argument(
        '-ss',
        '--slideshow',
        help='Instead of simply choosing a random pokemon ' +
             'from the filtered list, starts a slideshow (with X minutes ' +
             'of delay between pokemon) in the background with the ' +
             'pokemon that matched the filters',
        const=10.0, nargs='?', type=float, metavar='X')
    is_slideshow = '-ss' in sys.argv or '--slideshow' in sys.argv
    misc_group.add_argument(
        '-w',
        '--wallpaper',
        help='Changes the desktop wallpaper instead of the terminal '
             'background',
        action='store_true')
    misc_group.add_argument(
        '-v', '--verbose', help='Enables verbose output', action='store_true')
    misc_group.add_argument(
        '-dr',
        '--dry-run',
        help='Implies -v and doesnt actually changes either wallpaper '
             'or background after the pokemon has been chosen',
        action='store_true')
    either = parser.add_mutually_exclusive_group()
    either.add_argument(
        '-c',
        '--clear',
        help='Clears the current pokemon from terminal '
             'background and quits.',
        action='store_true')
    either.add_argument(
        'id',
        help='Specify the desired pokemon ID or the exact (case insensitive) name',
        nargs='?',
        default=0, const=0)
    options = parser.parse_args(argv)
    try:
        options.id = int(options.id)
    except ValueError as _:
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
            print("Time has to be greater then 0. (You can use decimals, e.g.: 0.1)")
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
