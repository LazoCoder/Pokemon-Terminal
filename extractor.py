# The logic for loading the Pokemon names and numbers from Data/pokemon.txt.

import printer
import os


# Load all the Pokemon and their corresponding numbers into a list.
def load_names():
    names_file = open(os.get_exec_path()[0] + "/Data/pokemon.txt", "r+")
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


# Find all the Pokemon who's names begin with a key word.
def pokemon_starting_with(word):
    all_pokemon = load_names()
    result = []
    for pokemon in all_pokemon:
        trimmed = trim_name(pokemon).lower()
        if trimmed.startswith(word):
            result.append(printer.add_zeroes(pokemon))
    return result


# Find all the Pokemon who's names begin with a key word.
def pokemon_containing(word):
    all_pokemon = load_names()
    result = []
    for pokemon in all_pokemon:
        trimmed = trim_name(pokemon).lower()
        if word in trimmed:
            result.append(printer.add_zeroes(pokemon))
    return result
