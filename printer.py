import backchanger

# Print the instructions of usage.
def print_usage():
    print("Incorrect arguments.")


# Print all the items in a list. Used for printing each Pokemon from a particular region.
def print_list(list_of_items):
    for item in list_of_items:
        print(item)


# Helper method for printing all the Pokemon in a particular region.
def print_region(i, j):
    pokemon_names = backchanger.load_names()
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