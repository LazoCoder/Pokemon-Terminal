# Module for printing various information.

import extractor


def print_usage():
    # Print the instructions of usage.
    print(
        '''
Usage:
    pokemon [parameter]

Parameters:
    [name]      -   Change the terminal background to the specified Pokemon.
    [index]     -   Change the terminal background to a Pokemon by its index.
    [region]    -   List all the Pokemon of the specified region.
    [letter]    -   List all Pokemon who's names begin with a particular letter.

Other Parameters:
    pokemon all         -   List all the Pokemon supported.
    pokemon random      -   Pick a Pokemon at random.
    pokemon regions     -   List all the available regions.
    pokemon slideshow   -   Iterate through each pokemon.
    pokemon help        -   Display this menu.
''')


def print_list(list_of_items):
    # Print all the items in a list. Used for printing each Pokemon from a particular region.
    for item in list_of_items:
        print(item)


def add_zeroes(pokemon):
    # Add zeros to the front so that it begins with 3 digits.
    # Example: "2 Ivysaur" -> "002 Ivysaur"
    zeroes = ""
    if int(pokemon.split(' ')[0]) < 10:
        zeroes = "00"
    elif int(pokemon.split(' ')[0]) < 100:
        zeroes = "0"
    return zeroes + pokemon


def print_columns(items, i, j):
    # Print a list as multiple columns instead of just one.
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


def print_region(i, j):
    # Helper method for printing all the Pokemon in a particular region.
    print_columns(extractor.load_names(), i, j)


def print_kanto():
    # Print each Kanto region Pokemon and its corresponding number.
    print_region(0, 151)


def print_johto():
    # Print each Johto region Pokemon and its corresponding number.
    print_region(151, 251)


def print_hoenn():
    # Print each Hoenn region Pokemon and its corresponding number.
    print_region(251, 386)


def print_sinnoh():
    # Print each Sinnoh region Pokemon and its corresponding number.
    print_region(386, 493)


def print_all():
    # Print all the Pokemon for all the regions supported.
    print_region(0, 493)


def print_pokemon_starting_with(char):
    # Print all the Pokemon who's names begin with a particular letter.
    pokemon = extractor.pokemon_starting_with(char)
    print_columns(pokemon, 0, len(pokemon))


def print_regions():
    # Print all the supported regions.
    print("Kanto")
    print("Johto")
    print("Hoenn")
    print("Sinnoh")
