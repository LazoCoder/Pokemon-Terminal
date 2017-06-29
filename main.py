#!/usr/bin/env python3

# The main module that brings everything together.

from sys import argv
from database import Database
import random
import scripter
import sys
import time


def print_list(list_of_items):
    # Print all the items in a list. Used for printing each Pokemon from a particular region.
    print("\n".join(str(item) for item in list_of_items))


def print_columns(items):
    # Print a list as multiple columns instead of just one.
    rows = []
    items_per_column = int(len(items) / 4) + 1
    for index, pokemon in enumerate(items):
        if not pokemon.is_extra():
            name = pokemon.get_id() + " " + str(pokemon.get_name()).capitalize()
        else:
            name = "--- " + pokemon.get_name()
        name = name.ljust(20)
        if len(rows) < items_per_column:
            rows.append(name)
        else:
            rows[index % items_per_column] += name
    print_list(rows)

def print_types(db):
    print("All existent pokemon types are: ")
    for x in db.get_pokemon_types():
        print(x + " - ", end='')
    print('\b\b\b   ')

def prefix_search(db, arg):
    # Find all Pokemon in database, db, with the prefix, arg.
    result = db.names_with_prefix(arg)
    if len(result) == 0:
        print("No Pokemon found with prefix '" + arg + "'.")
    else:
        print_columns(result)


def print_extra(db):
    # Print all the 'Extra' Pokemon from the 'Extra' folder.
    result = db.get_extra()
    if len(result) == 0:
        print("No Pokemon were found in Images/Extra.")
    else:
        print_columns(result)


def print_usage():
    # Print the instructions of usage.
    print(
        '''
Usage:
    pokemon [parameter]
    ichooseyou [parameter]

Parameters:
    [name]        -   Change the terminal background to the specified Pokemon.
    [index]       -   Change the terminal background to a Pokemon by its index.
    [region]      -   List all the Pokemon of the specified region.
    [one letter]  -   List all Pokemon who's names begin with a particular letter.
    [two letters] -   List all Pokemon who's names begin with those two letters.

Other Parameters:
    all                           -   List all the Pokemon supported.
    regions                       -   List all the available regions.
    extra                         -   List all the Pokemon from the 'Extra' folder.
    random                        -   Change the terminal background to a random Pokemon.
    random-<region>               -   Change the terminal background to a random Pokemon from the specified region.
    slideshow [time]              -   Iterate through each Pokemon. Optional time (in seconds) between Pokemon.
    slideshow-<region> [time]     -   Iterate through each Pokemon in the specified region. Optional time (in seconds) between Pokemon.
    rnd-slideshow [time]          -   Iterate through each Pokemon in a random order. Optional time (in seconds) between Pokemon.
    rnd-slideshow-<region> [time] -   Iterate through each Pokemon in the specified region in a random order. Optional time (in seconds) between Pokemon.
    light                         -   Change the terminal background to a random light-colored Pokemon.
    dark                          -   Change the terminal background to a random dark-colored Pokemon.
    type [type]                   -   Random pokemon of [type] omit the type for a list of types.
    clear | disable | off         -   Clear the Pokemon in the terminal.
    help                          -   Display this menu.

Wallpaper Parameters:
    pokemon _pikachu               -   Change the wallpaper to the specified Pokemon.
    pokemon _random                -   Change the wallpaper to a random Pokemon.
    pokemon _random-kanto          -   Change the wallpaper to a random Pokemon from the specified region.

Search System Information:
    Any input containing 3 or more characters triggers the internal search system. Examples:
    "pokemon pika" changes the terminal background to Pikachu.
    "pokemon dos"  changes the terminal background to Gyarados.
''')


def slideshow(db, start, end, seconds="0.25", rand=False):
    delay = 0.25
    if seconds is not None:
        delay = float(seconds)

    # Show each Pokemon, one by one.
    r = list(range(start, end))
    if rand:
        random.shuffle(r)
    try:
        for x in r:
            pokemon = db.get_pokemon(x)
            scripter.change_terminal(pokemon)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("Program was terminated.")
        sys.exit()


def change_terminal_background(db, arg):
    # Change the terminal background to the specified Pokemon, if it exists.
    if arg in db:
        pokemon = db.get_pokemon(arg)
        scripter.change_terminal(pokemon)
    else:  # If not found in the database, try to give suggestions.
        suggestions = db.names_with_infix(arg)
        if len(suggestions) == 0:
            print("No such Pokemon was found and no suggestions are available.")
        elif len(suggestions) == 1:
            scripter.change_terminal(suggestions[0])
            print("Did you mean " + suggestions[0].get_name().capitalize() + "?")
            scripter.change_terminal(suggestions[0])
        else:
            print("Did you mean " + suggestions[0].get_name().capitalize() + "?")
            print("Other suggestions:")
            print_columns(suggestions[1:])
            scripter.change_terminal(suggestions[0])


def change_wallpaper(db, arg):
    # Change the wallpaper to the specified Pokemon, if it exists.
    if arg in db:
        pokemon = db.get_pokemon(arg)
        scripter.change_wallpaper(pokemon)
    else:  # If not found in the database, try to give suggestions.
        suggestions = db.names_with_infix(arg)
        if len(suggestions) == 0:
            print("No such Pokemon was found and no suggestions are available.")
        elif len(suggestions) == 1:
            scripter.change_wallpaper(suggestions[0])
            print("Did you mean " + suggestions[0].get_name().capitalize() + "?")
            scripter.change_wallpaper(suggestions[0])
        else:
            print("Result: " + arg)
            print("Did you mean " + suggestions[0].get_name().capitalize() + "?")
            print("Other suggestions:")
            print_columns(suggestions[1:])
            scripter.change_wallpaper(suggestions[0])


def multiple_argument_handler(arg, arg2):
    db = Database()
    rand = arg.startswith("rnd")
    if "slideshow" in arg:
        try:
            if arg.endswith("slideshow"):
                slideshow(db, 1, 494, arg2, rand)
            elif arg.endswith("slideshow-kanto"):
                slideshow(db, 1, 152, arg2, rand)
            elif arg.endswith("slideshow-johto"):
                slideshow(db, 152, 252, arg2, rand)
            elif arg.endswith("slideshow-hoenn"):
                slideshow(db, 252, 387, arg2, rand)
            elif arg.endswith("slideshow-sinnoh"):
                slideshow(db, 387, 494, arg2, rand)
            else:
                print('Invalid slideshow command specified.'
                      '\nType "help" to see all the commands.')
        except ValueError:
            print('The slideshow time needs to be a positive number'
                  '\nType "help" to see all the commands.')
    elif arg.lower() == 'type':
        arg2 = arg2.lower()
        if arg2 not in db.get_pokemon_types():
            print("Invalid type specified")
        else:
            target = db.get_pokemon_of_type(arg2).get_name()
            if ESCAPE_CODE:
                change_wallpaper(db, target)
            else:
                change_terminal_background(db, target)
    else:
        print('Invalid command specified.'
              '\nType "help" to see all the commands.')


def single_argument_handler(arg):
    # Handle the logic for when there is only one command line parameter inputted.
    db = Database()

    if len(arg) < 3 and arg.isalpha():
        prefix_search(db, arg)
    elif arg == "extra":
        print_extra(db)
    elif arg == "regions":
        print_list(db.get_regions())
    elif arg == "help" or arg.startswith("-h"):
        print_usage()
    elif arg == "kanto":
        print_columns(db.get_kanto())
    elif arg == "johto":
        print_columns(db.get_johto())
    elif arg == "hoenn":
        print_columns(db.get_hoenn())
    elif arg == "sinnoh":
        print_columns(db.get_sinnoh())
    elif arg == "all":
        print_columns(db.get_all())
    elif arg in ("clear", "disable", "off"):
        scripter.clear_terminal()
    elif arg == "random" and ESCAPE_CODE:
        change_wallpaper(db, db.get_random().get_name())
    elif arg == "random-kanto" and ESCAPE_CODE:
        change_wallpaper(db, db.get_random_from_region("kanto").get_name())
    elif arg == "random-johto" and ESCAPE_CODE:
        change_wallpaper(db, db.get_random_from_region("johto").get_name())
    elif arg == "random-hoenn" and ESCAPE_CODE:
        change_wallpaper(db, db.get_random_from_region("hoenn").get_name())
    elif arg == "random-sinnoh" and ESCAPE_CODE:
        change_wallpaper(db, db.get_random_from_region("sinnoh").get_name())
    elif arg == "random":
        change_terminal_background(db, db.get_random().get_name())
    elif arg == "random-kanto":
        change_terminal_background(db, db.get_random_from_region("kanto").get_name())
    elif arg == "random-johto":
        change_terminal_background(db, db.get_random_from_region("johto").get_name())
    elif arg == "random-hoenn":
        change_terminal_background(db, db.get_random_from_region("hoenn").get_name())
    elif arg == "random-sinnoh":
        change_terminal_background(db, db.get_random_from_region("sinnoh").get_name())
    elif arg == "light" and ESCAPE_CODE:
        change_wallpaper(db, db.get_light().get_name())
    elif arg == "dark" and ESCAPE_CODE:
        change_wallpaper(db, db.get_dark().get_name())
    elif arg == "light":
        change_terminal_background(db, db.get_light())
    elif arg == "dark":
        change_terminal_background(db, db.get_dark())
    elif arg in ("type", "types"):
        print_types(db)
    elif arg == "slideshow":
        slideshow(db, 1, 494)
    elif arg == "slideshow-kanto":
        slideshow(db, 1, 152)
    elif arg == "slideshow-johto":
        slideshow(db, 152, 252)
    elif arg == "slideshow-hoenn":
        slideshow(db, 252, 387)
    elif arg == "slideshow-sinnoh":
        slideshow(db, 387, 494)
    elif arg.endswith("slideshow"):
        slideshow(db, 1, 494, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-kanto"):
        slideshow(db, 1, 152, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-johto"):
        slideshow(db, 152, 252, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-hoenn"):
        slideshow(db, 252, 387, rand=arg.startswith("rnd"))
    elif arg.endswith("slideshow-sinnoh"):
        slideshow(db, 387, 494, rand=arg.startswith("rnd"))
    elif arg == "?":
        print("This function is deprecated.")
    elif ESCAPE_CODE:
        change_wallpaper(db, arg)
    else:
        change_terminal_background(db, arg)

if __name__ == "__main__":
    # Entrance to the program.
    if len(argv) == 1:
        print('No command line arguments specified.'
              '\nTry typing in a Pokemon name or number.'
              '\nOr type "help" to see all the commands.')
        sys.exit(1)
    # If there is an escape code, then change the wallpaper, not the terminal.
    if str(argv[1]).startswith("_"):
        ESCAPE_CODE = True
    else:
        ESCAPE_CODE = False

    if len(argv) == 2:
        single_argument_handler(argv[1].lower())
    elif len(argv) == 3:
        multiple_argument_handler(argv[1].lower(), argv[2])
    else:
        print('Invalid number of arguments.'
              '\nType "help" to see all the commands.')
