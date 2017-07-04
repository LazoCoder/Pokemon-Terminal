# This module is for testing the different components of this project.

from database import Database
import sys


def print_items(items):
    # Print each item in a collection.
    for item in items:
        print(item)


def test_database_single_arg(arg):
    # Test the database where there is a single command line parameter.
    # The parameter is the name of the method to test.
    arg = arg[1].lower()
    db = Database()
    if arg == "__str__":
        print(db)
    elif arg == "__len__":
        print(len(db))
    elif arg == "get_all":
        print_items(db.get_all())
    elif arg == "get_regions":
        print_items(db.get_regions())
    elif arg == "get_kanto":
        print_items(db.get_kanto())
    elif arg == "get_johto":
        print_items(db.get_johto())
    elif arg == "get_hoenn":
        print_items(db.get_hoenn())
    elif arg == "get_sinnoh":
        print_items(db.get_sinnoh())
    elif arg == "get_extra":
        print_items(db.get_extra())
    elif arg == "get_random":
        print(db.get_random())
    else:
        print("No such public method '" + arg + "' with zero parameters exists in the Database class.")


def test_database_double_arg(arg):
    # Test the database where there are two command line parameters.
    # The first parameter is the name of the method to test.
    # The second parameter is the input parameter for the method that is being test.
    arg1 = arg[1].lower()
    arg2 = arg[2].lower()
    db = Database()
    if arg1 == "__contains__":
        print(arg2 in db)
    elif arg1 == "pokemon_id_exists":
        print(db.pokemon_id_exists(arg2))
    elif arg1 == "pokemon_name_exists":
        print(db.pokemon_name_exists(arg2))
    elif arg1 == "get_pokemon":
        print(db.get_pokemon(arg2))
    elif arg1 == "get_pokemon_by_name":
        print(db.get_pokemon_by_name(arg2))
    elif arg1 == "get_pokemon_by_id":
        print(db.get_pokemon_by_id(arg2))
    elif arg1 == "names_with_prefix":
        print_items(db.names_with_prefix(arg2))
    elif arg1 == "names_with_infix":
        print_items(db.names_with_infix(arg2))
    elif arg1 == "get_light":
        print_items(db.get_light(threshold=int(arg2)/10, all_pkmn=True))
    elif arg1 == "get_dark":
        print_items(db.get_dark(threshold=int(arg2)/10, all_pkmn=True))
    else:
        print("No such public method '" + arg + "' with two parameters"
              " exists in the Database class.")


def main(argv):
    if len(argv) == 1:
        print("No command line parameters provided.")
    elif len(argv) == 2:
        test_database_single_arg(argv)
    elif len(argv) == 3:
        test_database_double_arg(argv)
    else:
        print("This module only takes one command line parameter.")


if __name__ == "__main__":
    main(sys.argv)
