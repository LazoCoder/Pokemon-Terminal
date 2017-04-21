from sys import argv
import time
import printer
import backchanger


# Test each Pokemon in order, one by one.
def debug():
    for x in range(1, 494):
        backchanger.change_background(x)
        time.sleep(0.25)


# Entrance to the program.
if __name__ == "__main__":
    if len(argv) == 2:
        arg = argv[1].lower()
        if arg == "kanto":
            printer.print_kanto()
        elif arg == "johto":
            printer.print_johto()
        elif arg == "hoenn":
            printer.print_hoenn()
        elif arg == "sinnoh":
            printer.print_sinnoh()
        elif arg == "debug":
            debug()
        else:
            backchanger.change_background(argv[1])
    else:
        printer.print_usage()
