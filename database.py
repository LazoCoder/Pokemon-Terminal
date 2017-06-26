# The Database object is a container for all the supported Pokemon.

import os
import random


class Pokemon:
    __id = ""  # ID is stored as a string because it must maintain "003" format, not "3".
    __name = ""
    __region = ""
    __path = ""  # The location of the image.
    __dark_threshold = 0.5

    def __init__(self, identifier, name, region, path, dark_threshold):
        self.__id = identifier
        self.__name = name
        self.__region = region
        self.__path = path
        self.__dark_threshold = dark_threshold

    def get_id(self):
        # Pokemon from folder 'Extra' have no ID.
        return "---" if self.is_extra() else self.__id

    def get_name(self):
        return self.__name

    def get_region(self):
        return self.__region

    def get_path(self):
        return self.__path

    @property
    def dark_threshold(self):
        return self.__dark_threshold

    def is_extra(self):
        return self.__id is None

    def __str__(self):
        if self.is_extra():
            return "--- " + self.get_name().capitalize() + " at " + self.get_path()
        else:
            return self.get_id() + " " + self.get_name().capitalize() + " at " + self.get_path()


class Database:
    __pokemon_list = []
    __pokemon_dictionary = {}
    __directory = ""  # The global location of the code.
    __MAX_ID = 493  # Highest possible Pokemon ID.
    __regions = ('kanto', 'johto', 'hoenn', 'sinnoh')

    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.__load_data()
        self.__load_extra()

    def __str__(self):
        return "\n".join(str(element) for element in self.__pokemon_list)

    def __contains__(self, pokemon):
        # Check for a Pokemon by ID or name.
        if isinstance(pokemon, int) or str(pokemon).isdigit():
            return self.pokemon_id_exists(int(pokemon))
        else:
            return self.pokemon_name_exists(pokemon)

    def __len__(self):
        return len(self.__pokemon_list)

    def get_all(self):
        # Get all the Pokemon.
        return [pokemon for pokemon in self.__pokemon_list]
        # or... return self.__pokemon_list[:]  # return a copy of self.__pokemon_list

    def get_regions(self):
        # Get all the supported regions.
        return self.__regions

    def get_kanto(self):
        # Get all the Pokemon from the Kanto region.
        return self.__get_region("kanto")

    def get_johto(self):
        # Get all the Pokemon from the Johto region.
        return self.__get_region("johto")

    def get_hoenn(self):
        # Get all the Pokemon from the Hoenn region.
        return self.__get_region("hoenn")

    def get_sinnoh(self):
        # Get all the Pokemon from the Sinnoh region.
        return self.__get_region("sinnoh")

    def get_extra(self):
        # Get all the Extra Pokemon images available.
        return self.__get_region(None)

    def get_light(self, threshold=0.4, all=False):
        light = [pokemon.__name for pokemon in self.__pokemon_list
                 if pokemon.dark_threshold > threshold]
        return light if all else random.choice(light)

    def get_dark(self, threshold=0.6, all=False):
        dark = [pokemon.__name for pokemon in self.__pokemon_list
                if pokemon.dark_threshold < threshold]
        return dark if all else random.choice(dark)

    def __get_region(self, region):
        # Helper method for getting all the Pokemon of a specified region.
        return [pokemon for pokemon in self.__pokemon_list
                if pokemon.get_region() == region]

    def get_random(self):
        # Select a random Pokemon from the database.
        return random.choice(self.__pokemon_list)

    def get_random_from_region(self, region):
        # Get a random Pokemon from a specific region.
        return random.choice(self.__get_region(region))

    def pokemon_id_exists(self, identifier):
        # Check for Pokemon by ID.
        identifier = int(identifier)
        return 0 < identifier <= self.__MAX_ID

    def pokemon_name_exists(self, name):
        # Check for Pokemon by Name.
        return name.lower() in self.__pokemon_dictionary

    def get_pokemon(self, pokemon):
        # Get a Pokemon by name or ID.
        if not isinstance(pokemon, (int, str)):
            raise Exception("The parameter Pokemon must be of type integer or string.")
        if pokemon not in self:
            raise Exception("No such Pokemon in the database.")
        if isinstance(pokemon, int) or str(pokemon).isdigit():
            return self.get_pokemon_by_id(int(pokemon))
        else:
            return self.get_pokemon_by_name(pokemon)

    def get_pokemon_by_name(self, name):
        # Get a Pokemon by its name.
        if not isinstance(name, str):
            raise TypeError("The type of name must be a string.")
        if not self.pokemon_name_exists(name):
            raise Exception("No such Pokemon in the database.")
        return self.__pokemon_dictionary[name]

    def get_pokemon_by_id(self, identifier):
        # Get a Pokemon by its ID.
        if not isinstance(identifier, int) and not str(identifier).isdigit():
            raise TypeError("The Pokemon ID must be a number.")
        identifier = int(identifier)
        if not self.pokemon_id_exists(identifier):
            raise Exception("The Pokemon ID must be between 1 and " + str(self.__MAX_ID) + " inclusive.")
        return self.__pokemon_list[identifier - 1]  # Subtract 1 to convert to 0 base indexing.

    def names_with_prefix(self, prefix):
        # Return Pokemon who's names begin with the specified prefix.
        return [pokemon for pokemon in self.__pokemon_list
                if str(pokemon.get_name()).startswith(prefix)]

    def names_with_infix(self, infix):
        # Return Pokemon who's names contains the specified infix.
        return [pokemon for pokemon in self.__pokemon_list
                if infix in str(pokemon.get_name())]

    def __load_data(self):
        """Load all the Pokemon data. This does not include the 'Extra' Pokemon."""
        with open(self.directory + "/./Data/light-dark.txt", 'r') as data_file:
            for i, line in enumerate(data_file):
                name, _, dark_threshold = line.strip().partition(' ')
                id = i + 1  # zero-based indexing --> one-based sequence numbers
                identifier = '{:03}'.format(id)  # zero padded string
                region = self.__determine_region(id)
                path = self.__determine_folder(id) + "/" + identifier + ".jpg"
                pokemon = Pokemon(identifier, name.lower(), region, path, dark_threshold)
                self.__pokemon_list.append(pokemon)
                self.__pokemon_dictionary[pokemon.get_name()] = pokemon

    def __load_extra(self):
        """Load all the file names of the images in the Extra folder."""
        for file in os.listdir(self.directory + "/./Images/Extra"):
            if file.endswith(".jpg"):
                name = os.path.join("/Images/Extra", file).split('/')[-1][0:-4].lower()
                path = self.directory + "/./Images/Extra/" + name + ".jpg"
                dark_threshold = 0.5  # TODO: what should this be for an extra?
                pokemon = Pokemon(None, name, None, path, dark_threshold)
                if name in self.__pokemon_dictionary:
                    raise Exception("Duplicate names detected. "
                                    "The name of the file " + str(name) + ".jpg in the folder 'Extra' must be changed.")
                self.__pokemon_list.append(pokemon)
                self.__pokemon_dictionary[pokemon.get_name()] = pokemon

    def __determine_region(self, identifier):
        """Determine which region a Pokemon is from."""
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
        """Determine which folder a Pokemon is from."""
        suffix_dict = {"kanto": "I - Kanto",
                       "johto": "II - Johto",
                       "hoenn": "III - Hoenn",
                       "sinnoh": "IV - Sinnoh"}
        suffix = suffix_dict.get(self.__determine_region(identifier))
        return "{}/./Images/Generation {}".format(self.directory, suffix)
