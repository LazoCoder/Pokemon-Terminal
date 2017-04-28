#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5

# The main module that brings everything together.

from sys import argv
from database import Pokemon, Database
import scripter


def print_list(list_of_items):
    # Print all the items in a list. Used for printing each Pokemon from a particular region.
    for item in list_of_items:
        print(item)


def print_columns(items):
    # Print a list as multiple columns instead of just one.
    rows = []
    items_per_column = int(len(items) / 4) + 1

    for index in range(0, len(items)):
        pokemon = items[index]

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

Parameters:
    [name]        -   Change the terminal background to the specified Pokemon.
    [index]       -   Change the terminal background to a Pokemon by its index.
    [region]      -   List all the Pokemon of the specified region.
    [one letter]  -   List all Pokemon who's names begin with a particular letter.
    [two letters] -   List all Pokemon who's names begin with those two letters.

Other Parameters:
    pokemon all             -   List all the Pokemon supported.
    pokemon random          -   Change terminal background to a random Pokemon.
    pokemon .random         -   Change desktop wallpaper to a random Pokemon.
    pokemon ?               -   Identify the current Pokemon in the terminal.
    pokemon .?              -   Identify the current Pokemon in the wallpaper.
    pokemon regions         -   List all the available regions.
    pokemon extra           -   List all the Pokemon from the 'Extra' folder.
    pokemon slideshow       -   Iterate through each Pokemon.
    pokemon slideshow-kanto -   Iterate through each Pokemon in the specified reigon.
    pokemon help            -   Display this menu.
''')


def change_terminal_background(db, arg):
    # Change the terminal background to the specified Pokemon, if it exists.
    if arg in db:
        pokemon = db.get_pokemon(arg)
        scripter.change_terminal(pokemon)
    else:
        print("No such Pokemon was found.")


def change_wallpaper(db, arg):
    # Change the wallpaper to the specified Pokemon, if it exists.
    if arg in db:
        pokemon = db.get_pokemon(arg)
        scripter.change_wallpaper(pokemon)
    else:
        print("No such Pokemon was found.")


def single_argument_handler(arg):
    # Handle the logic for when there is only one command line parameter inputted.
    db = Database()
    if len(arg) < 3 and arg.isalpha():
        prefix_search(db, arg)
    elif arg == "extra" or arg == "custom":
        print_extra(db)
    elif arg == "regions":
        print_list(db.get_regions())
    elif arg == "help" or arg == "--help" or arg == "-h":
        print_usage()
    elif arg == "kanto":
        print_columns(db.get_kanto())
    elif arg == "johto":
        print_columns(db.get_johto())
    elif arg == "hoenn":
        print_columns(db.get_hoenn())
    elif arg == "sinnoh":
        print_columns(db.get_sinnoh())
    elif arg == "all" or arg == "pokemon" or arg == "list":
        print_columns(db.get_all())
    elif arg == "rand" or arg == "random":
        change_terminal_background(db, db.get_random().get_name())
    elif arg == ".rand" or arg == ".random":
        pokemon = db.get_random()
        change_wallpaper(db, pokemon.get_name())
    elif str(arg).startswith("."):
        change_wallpaper(db, arg[1:])
    else:
        change_terminal_background(db, arg)


if __name__ == "__main__":
    # Entrance to the program.
    if len(argv) == 1:
        print("No command line arguments specified. Try typing in a Pokemon name or number.")
    elif len(argv) == 2:
        single_argument_handler(argv[1].lower())
    else:
        print("Only one command line argument is supported.")
