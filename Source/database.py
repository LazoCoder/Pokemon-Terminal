# The Database object is a container for all the supported Pokemon. It loads up all the Pokemons'
# IDs and names from a text file. It also analyzes all the images available in the 'Extra' folder
# and stores them in a separate data structure. The Pokemon in the text file are already assumed
# to exist in the other folders, so there is no reason to traverse them.
#
# The Pokemon are stored as Pokemon objects in a list. They contain an ID, name, region, and
# folder location. The 'Extra' Pokemon images are stored as tuples in a separate list. The
# reason for this is because 'Extra' images don't have IDs. The tuple contains the name of
# the image and the location of the image.

import os
from sys import argv


class Pokemon:
    __id = ""  # ID is stored as a string because it must maintain "003" format, not "3".
    __name = ""
    __region = ""
    __folder = ""  # The location of the image.

    def __init__(self, identifier, name, region, folder):
        self.__id = identifier
        self.__name = name
        self.__region = region
        self.__folder = folder

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_region(self):
        return self.__region

    def get_folder(self):
        return self.__folder

    def __str__(self):
        return self.get_id() + " " + self.get_name() + " at " + self.get_folder()


class Database:
    __pokemon_list = []
    __pokemon_dictionary = {}
    __extra_pokemon = {}  # The Pokemon from the 'Extra' folder.
    __directory = ""  # The global location of the code.
    __MAX_ID = 493  # Highest possible Pokemon ID.

    def __init__(self):
        self.directory = os.get_exec_path()[0]
        self.__load_data()
        self.__load_extra()

    def __str__(self):
        string = "POKEMON:\n"
        for element in self.__pokemon_list:
            string += str(element) + "\n"
        string += "EXTRA:\n"
        for element in self.__extra_pokemon:
            string += str(element) + " in " + str(self.__extra_pokemon[element] + "\n")
        return string[:-1]  # Remove the final new line ("\n").

    def pokemon_exists(self, pokemon):
        # Check for a Pokemon by ID or name.
        if type(pokemon) is int or str(pokemon).isdigit():
            return self.id_exists(pokemon)
        else:
            return self.name_exists(pokemon)

    def id_exists(self, identifier):
        # Check for Pokemon by ID.
        identifier = int(identifier)
        if identifier < 1 or identifier > self.__MAX_ID:
            return False
        else:
            return True

    def name_exists(self, name):
        # Check for Pokemon by Name.
        if name.lower() in self.__pokemon_dictionary:
            return True
        if name.lower() in self.__extra_pokemon:
            return True
        return False

    def __load_data(self):
        # Load all the Pokemon data. This does not include the 'Extra' Pokemon.
        path = self.directory + "/./Data/pokemon.txt"
        data_file = open(path, "r+")
        for line in data_file:  # Load everything but the Pokemon from the 'Extra' folder.
            identifier = line.split(' ')[0]  # First part of the line is the id.
            name = line[len(identifier)+1:-1].lower()  # The rest is the name (minus the new line at the end).
            identifier = self.__add_zeroes(identifier)  # This statement cannot occur before name has been created.
            region = self.__determine_region(identifier)
            folder = self.__determine_folder(identifier)
            pokemon = Pokemon(identifier, name, region, folder)
            self.__pokemon_list.append(pokemon)
            self.__pokemon_dictionary[pokemon.get_name()] = pokemon

    def __load_extra(self):
        # Load all the file names of the images in the Extra folder.
        for file in os.listdir(self.directory + "/./Images/Extra"):
            if file.endswith(".png"):
                name = os.path.join("/Images/Extra", file).split('/')[-1][0:-4].lower()
                folder = self.directory + "/./Images/Extra"
                self.__extra_pokemon[name] = folder

    @staticmethod
    def __add_zeroes(number):
        # Add zeroes to the front so that it begins with 3 digits. Example: "2" -> "002".
        zeroes = ""
        if int(number) < 10:
            zeroes = "00"
        elif int(number) < 100:
            zeroes = "0"
        return zeroes + str(number)

    def __determine_region(self, identifier):
        # Determine which region a Pokemon is from.
        identifier = int(identifier)
        if identifier < 1:
            raise Exception("Pokemon ID cannot be less than 1.")
        if identifier < 152:
            return "kanto"
        elif identifier < 252:
            return "johto"
        elif identifier < 387:
            return "hoenn"
        elif identifier < 494:
            return "sinnoh"
        else:
            raise Exception("Pokemon ID cannot be greater than 493.")

    def __determine_folder(self, identifier):
        # Determine which folder a Pokemon is from.
        identifier = int(identifier)
        if identifier < 1:
            raise Exception("Pokemon ID cannot be less than 1.")
        if identifier < 152:
            return self.directory + "/./Images/Generation I - Kanto"
        elif identifier < 252:
            return self.directory + "/./Images/Generation II - Johto"
        elif identifier < 387:
            return self.directory + "/./Images/Generation III - Hoenn"
        elif identifier < 494:
            return self.directory + "/./Images/Generation IV - Sinnoh"
        else:
            raise Exception("Pokemon ID cannot be greater than 493.")

# Method for debugging.
if __name__ == "__main__":
    database = Database()
    if len(argv) == 1:
        print(database)
    else:
        print(database.pokemon_exists(argv[1]))
