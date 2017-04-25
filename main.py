#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5

# The main module that brings everything together.

from sys import argv
import backchanger
import extractor
import printer
import random
import sys
import time


def debug():
    # Test each Pokemon in order, one by one.
    for x in range(1, 494):
        backchanger.change_background(x)
        try:
            time.sleep(0.25)
        except KeyboardInterrupt:
            print("Program was terminated.")
            sys.exit()


if __name__ == "__main__":
    # Entrance to the program.
    if len(argv) == 1:
        print("No command line arguments specified. Try typing in a Pokemon name or number.")
    elif len(argv) == 2:
        arg = argv[1].lower()
        if len(arg) == 1 and arg.isalpha():
            printer.print_pokemon_starting_with(arg)
        elif arg == "regions":
            printer.print_regions()
        elif arg == "--help" or arg == "help" or arg == "-h":
            printer.print_usage()
        elif arg == "kanto":
            printer.print_kanto()
        elif arg == "johto":
            printer.print_johto()
        elif arg == "hoenn":
            printer.print_hoenn()
        elif arg == "sinnoh":
            printer.print_sinnoh()
        elif arg == "all" or arg == "pokemon" or arg == "list":
            printer.print_all()
        elif arg == "slideshow":
            debug()
        elif arg == "rand" or arg == "random":
            backchanger.change_background(random.randint(1, 494))
        elif arg == "?" or arg == "current":
            extractor.current_pokemon()
        else:
            backchanger.change_background(arg)
    else:
        print("Only one command line argument is supported.")
