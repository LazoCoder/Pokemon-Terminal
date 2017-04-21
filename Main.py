import os
from sys import argv
import time


# Determine which region a Pokemon is from.
def get_region(pokemon_number):
    if pokemon_number < 1:
        raise Exception("Pokemon number must be at least 1.")
    if pokemon_number < 152:
        return "Generation I - Kanto"
    elif pokemon_number < 252:
        return "Generation II - Johto"
    elif pokemon_number < 387:
        return "Generation III - Hoenn"
    elif pokemon_number < 494:
        return "Generation IV - Sinnoh"
    else:
        raise Exception("Pokemon number must be less than 494.")


# Append zeros at the front if necessary and add the extension.
# Example: 5 would become 005.png.
def get_filename(pokemon_number):
    if pokemon_number < 1:
        raise Exception("Pokemon number must be at least 1.")
    elif pokemon_number < 10:
        return "00" + str(pokemon_number) + ".png"
    elif pokemon_number < 100:
        return "0" + str(pokemon_number) + ".png"
    elif pokemon_number < 494:
        return str(pokemon_number) + ".png"
    else:
        raise Exception("Pokemon number must be less than 494.")


# Create the script that will change the terminal background image.
def create_applescript_content(region, filename):
    content = "tell application \"iTerm\"\n"
    content += "\ttell current session of current window\n"
    content += "\t\tset background image to \"" + os.getcwd() + "/Images/" + region + "/" + filename + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


# Create and save the script for changing the terminal background image.
def create_applescript(pokemon_number):
    region = get_region(pokemon_number)
    filename = get_filename(pokemon_number)
    content = create_applescript_content(region, filename)
    file = open("Scripts/background.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


# Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
def create_bash_run():
    content = "#!/bin/bash\n" + "osascript " + os.getcwd() + "/Scripts/background.scpt"
    if open("Scripts/run.sh", 'r').read() == content:
        return
    file = open("Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


# Load all the Pokemon and their corresponding numbers into a list.
def load_names():
    names_file = open("Data/pokemon.txt", "r+")
    content = names_file.readlines()
    return content


# Extract the name from a Pokemon extracted from the data file.
# Example: it will be read in from the data file as "150 Mewtwo\n" but it should just be "Mewtwo".
def trim_name(pokemon):
    front_trim = 0
    for char in pokemon:
        if not char.isalpha():
            front_trim += 1
        else:
            break
    return pokemon[front_trim:-1]


# Convert a Pokemon name to a number.
# Example: Pikachu returns 25. If the Pokemon does not exist, return -1.
def to_number(pokemon_name):
    pokemon_names = load_names()
    pokemon_name = pokemon_name.lower()
    for pokemon in pokemon_names:
        trimmed_name = trim_name(pokemon).lower()
        if pokemon_name == trimmed_name:
            return int(pokemon.split(' ')[0])
    return -1


# Print the instructions of usage.
def print_usage():
    print("Incorrect arguments.")


# Print all the items in a list. Used for printing each Pokemon from a particular region.
def print_list(list):
    for item in list:
        print(item)


# Helper method for printing all the Pokemon in a particular region.
def print_region(i, j):
    pokemon_names = load_names()
    names = []
    pokemon_per_list = int((j - i) / 3) + 1

    for index in range(i, j):
        name = pokemon_names[index][:-1]

        # For formatting.
        if len(name) < 10:
            name += "     "

        if len(names) < pokemon_per_list:
            names.append(name)
        else:
            names[(index - i) % pokemon_per_list] += "\t\t" + name

    print_list(names)


# Print each Kanto region Pokemon and its corresponding number.
def print_kanto():
    print_region(0, 151)


# Print each Johto region Pokemon and its corresponding number.
def print_johto():
    print_region(151, 251)


# Print each Hoenn region Pokemon and its corresponding number.
def print_hoenn():
    print_region(251, 386)


# Print each Sinnoh region Pokemon and its corresponding number.
def print_sinnoh():
    print_region(386, 493)


# Changes the background image in the terminal.
# The parameter is the Pokemon name or number.
def change_background(pokemon):
    if str(pokemon).isdigit():
        pokemon = int(pokemon)
        if pokemon < 1 or pokemon > 493:
            print("Only pokemon 1 through 493 are supported.")
            return
        create_applescript(pokemon)
    else:
        number = to_number(pokemon)
        if number == -1:
            print("\"" + pokemon + "\" is not a supported Pokemon or Region.")
            return
        create_applescript(number)
    create_bash_run()
    os.system('Scripts/run.sh')


# Test each Pokemon in order, one by one.
def debug():
    for x in range(1, 494):
        change_background(x)
        time.sleep(0.25)


# Entrance to the program.
if __name__ == "__main__":
    if len(argv) == 2:
        arg = argv[1].lower()
        if arg == "kanto":
            print_kanto()
        elif arg == "johto":
            print_johto()
        elif arg == "hoenn":
            print_hoenn()
        elif arg == "sinnoh":
            print_sinnoh()
        elif arg == "debug":
            debug()
        else:
            change_background(argv[1])
    else:
        print_usage()
