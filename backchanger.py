import filegen
import os


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


# Changes the background image in the terminal.
# The parameter is the Pokemon name or number.
def change_background(pokemon):
    if str(pokemon).isdigit():
        pokemon = int(pokemon)
        if pokemon < 1 or pokemon > 493:
            print("Only pokemon 1 through 493 are supported.")
            return
        filegen.create_applescript(pokemon)
    else:
        number = to_number(pokemon)
        if number == -1:
            print("\"" + pokemon + "\" is not a supported Pokemon or Region.")
            return
        filegen.create_applescript(number)
    filegen.create_bash_run()
    os.system('Scripts/run.sh')