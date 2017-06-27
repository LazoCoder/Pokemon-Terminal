# This module is for testing the different components of this project.

from database import Database
from sys import argv
import pytest


def print_items(items):
    # Print each item in a collection.
    for item in items:
        print(item)


def _test_database_single_arg(arg):
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


def _test_database_double_arg(arg):
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
    else:
        print("No such public method '" + arg + "' with two parameters exists in the Database class.")


def test_no_args():
    assert main() == "No command line parameters provided."

    
def test_len():
    assert main('__len__') == db.Database.__MAX_ID


def test_three_args():
    assert main(1, 2, 3) == "This module only accepts one or two command line parameters."
    

def main(args:
    if len(args) == 0:
        print("No command line parameters provided.")
    elif len(argv) == 1:
        _test_database_single_arg(args)
    elif len(argv) == 2:
        _test_database_double_arg(args)
    else:
        print("This module only accepts one or two command line parameters.")

if __name__ == "__main__":
    return main(argv[1:])
