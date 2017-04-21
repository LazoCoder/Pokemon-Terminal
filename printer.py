# Module for printing various information.

import extractor


# Print the instructions of usage.
def print_usage():
    print(
        '''
Usage:
    python3.5 main.py [Pokemon name]
    python3.5 main.py [Pokemon index]
    python3.5 main.py [region]
    python3.5 main.py [one letter]

Parameter Explanations:
    [Pokemon name]  -   Changes the terminal background to the specified Pokemon.
    [Pokemon index] -   Changes the terminal background to a Pokemon by its index.
    [region]        -   Print all the Pokemon of the specified region.
    [one letter]    -   Print all Pokemon who's names begin with a particular letter.

Examples:
    [Pokemon name]  -   python3.5 main.py pikachu
    [Pokemon index] -   python3.5 main.py 25
    [region]        -   python3.5 main.py johto
    [one letter]    -   python3.5 main.py k
        ''')


# Print all the items in a list. Used for printing each Pokemon from a particular region.
def print_list(list_of_items):
    for item in list_of_items:
        print(item)


# Add zeros to the front so that it begins 3 digits.
# Example: "2 Ivysaur" -> "002 Ivysaur"
def add_zeroes(pokemon):
    zeroes = ""
    if int(pokemon.split(' ')[0]) < 10:
        zeroes = "00"
    elif int(pokemon.split(' ')[0]) < 100:
        zeroes = "0"
    return zeroes + pokemon


# Print a list as multiple columns instead of just one.
def print_columns(items, i, j):
    rows = []
    items_per_column = int((j - i) / 3) + 1

    for index in range(i, j):
        name = items[index][:-1]

        # For formatting: this helps line up columns correctly where a short name would otherwise ruin it.
        if len(name) < 10:
            name += "   "

        if len(rows) < items_per_column:
            rows.append(name)
        else:
            rows[(index - i) % items_per_column] += "\t\t" + name

    print_list(rows)


# Helper method for printing all the Pokemon in a particular region.
def print_region(i, j):
    print_columns(extractor.load_names(), i, j)


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


# Print all the Pokemon for all the regions supported.
def print_all():
    print_region(0, 493)


# Print all the Pokemon who's names begin with a particular letter.
def print_pokemon_starting_with(char):
    pokemon = extractor.pokemon_starting_with(char)
    print_columns(pokemon, 0, len(pokemon))


# Print all the supported regions.
def print_regions():
    print("Kanto")
    print("Johto")
    print("Hoenn")
    print("Sinnoh")
