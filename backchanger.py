# The logic for changing the terminal background.

import extractor
import filegen
import os
import sys


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


# Find Pokemon who's name starts with a word.
# Example: If user_input is "pika", the result will be Pikachu.
def guess_by_startswith(user_input):
    guessed_pokemon = extractor.pokemon_starting_with(user_input)
    if len(guessed_pokemon) == 0:
        return False
    print("Did you mean " + extractor.trim_name(guessed_pokemon[0]) + "?")
    if len(guessed_pokemon) > 1:
        print("Other suggestions:")
        for item in range(1, len(guessed_pokemon)):
            print(guessed_pokemon[item][:-1])
    digit_handler(int(guessed_pokemon[0].split(' ')[0]))
    return True


# Find Pokemon who's name contains a word.
# Example: If user input is "chu", the result will be Pikachu, Raichu, Pichu and Smoochum.
def guess_by_contains(user_input):
    guessed_pokemon = extractor.pokemon_containing(user_input)
    if len(guessed_pokemon) == 0:
        return False
    print("Did you mean " + extractor.trim_name(guessed_pokemon[0]) + "?")
    if len(guessed_pokemon) > 1:
        print("Other suggestions:")
        for item in range(1, len(guessed_pokemon)):
            print(guessed_pokemon[item][:-1])
    digit_handler(int(guessed_pokemon[0].split(' ')[0]))
    return True


# If no Pokemon is found by the user input then try to guess what Pokemon they meant.
# Return false if it failed to make any guesses.
def guess(user_input):
    if len(user_input) < 3:
        return guess_by_startswith(user_input)
    else:
        return guess_by_contains(user_input)


# Logic for dealing with user input when a Pokemon index is specified.
def digit_handler(user_input):
    user_input = int(user_input)
    if user_input < 1 or user_input > 493:
        print("Only pokemon 1 through 493 are supported.")
        return
    filegen.create_applescript(user_input)


# Logic for dealing with user input when a Pokemon name is specified.
def other_handler(user_input):
    number = to_number(user_input)
    if number == -1:
        guessed = guess(user_input)
        if not guessed:
            print("\"" + user_input, end="")
            print("\" is not a supported Pokemon or Region and no suggestions are available.")
            sys.exit()
        else:
            return
    else:
        filegen.create_applescript(number)


# Changes the background image in the terminal.
# The parameter is the Pokemon name or number.
def change_background(user_input):
    if str(user_input).isdigit():
        digit_handler(user_input)
    else:
        other_handler(user_input)
    filegen.create_bash_run()
    os.system(os.get_exec_path()[0] + "/Scripts/run.sh")
