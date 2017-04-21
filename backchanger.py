# The logic for changing the terminal background.

import extractor
import filegen
import os


# Convert a Pokemon name to a number.
# Example: Pikachu returns 25. If the Pokemon does not exist, return -1.
def to_number(pokemon_name):
    pokemon_names = extractor.load_names()
    pokemon_name = pokemon_name.lower()
    for pokemon in pokemon_names:
        trimmed_name = extractor.trim_name(pokemon).lower()
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
