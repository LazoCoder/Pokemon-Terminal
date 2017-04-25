# The logic for loading the Pokemon names and numbers from Data/pokemon.txt.

import printer
import os


def load_names():
    # Load all the Pokemon and their corresponding numbers into a list.
    names_file = open(os.get_exec_path()[0] + "/Data/pokemon.txt", "r+")
    content = names_file.readlines()
    return content


def trim_name(pokemon):
    # Extract the name from a Pokemon extracted from the data file.
    # Example: it will be read in from the data file as "150 Mewtwo\n" but it should just be "Mewtwo".
    front_trim = 0
    for char in pokemon:
        if not char.isalpha():
            front_trim += 1
        else:
            break
    return pokemon[front_trim:-1]


def pokemon_starting_with(word):
    # Find all the Pokemon who's names begin with a key word.
    all_pokemon = load_names()
    result = []
    for pokemon in all_pokemon:
        trimmed = trim_name(pokemon).lower()
        if trimmed.startswith(word):
            result.append(printer.add_zeroes(pokemon))
    return result


def pokemon_containing(word):
    # Find all the Pokemon who's names begin with a key word.
    all_pokemon = load_names()
    result = []
    for pokemon in all_pokemon:
        trimmed = trim_name(pokemon).lower()
        if word in trimmed:
            result.append(printer.add_zeroes(pokemon))
    return result


def current_pokemon():
    # Get the current Pokemon that is in the background.
    content = open(os.get_exec_path()[0] + "/Scripts/background.scpt", "r+").readlines()
    pokemon_id = content[2][len(content[2])-9:-6]
    all_pokemon = load_names()
    for pokemon in all_pokemon:
        if int(pokemon.split(' ')[0]) == int(pokemon_id):
            print(pokemon[:-1])  # Remove the new line at the end.
            break
