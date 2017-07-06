"""This files the loading of the pokemon database and the pokemon object"""

import os
import random


class Pokemon:
    """Class to represent pokemons"""
    # ID is stored as a string because it must maintain "003" format, not "3".
    __id = ""
    __name = ""
    __region = ""
    __path = ""  # The location of the image.
    __pkmn_type = ""
    __pkmn_type_secondary = ""
    __dark_threshold = 0.5

    def __init__(self, identifier, name, region, path, pkmn_type,
                 pkmn_type_secondary, dark_threshold):
        self.__id = identifier
        self.__name = name
        self.__region = region
        self.__path = path
        self.__dark_threshold = float(dark_threshold)
        self.__pkmn_type = pkmn_type
        self.__pkmn_type_secondary = pkmn_type_secondary

    def get_id(self):
        # Pokemon from folder 'Extra' have no ID.
        return self.__id or "---"

    def get_name(self):
        return self.__name

    def get_region(self):
        return self.__region

    def get_path(self):
        return self.__path

    def get_pkmn_type(self):
        return self.__pkmn_type

    def get_pkmn_type_secondary(self):
        return self.__pkmn_type_secondary

    def get_dark_threshold(self):
        return self.__dark_threshold

    def is_extra(self):
        return self.__id is None

    def __str__(self):
        name = self.get_name().title()
        return self.get_id() + " " + name + " at " + self.get_path()


class Database:
    """The Database object is a container for all the supported Pokemon."""
    __POKEMON_TYPES = ('normal', 'fire', 'fighting', 'water', 'flying',
                       'grass', 'poison', 'electric', 'ground', 'psychic',
                       'rock', 'ice', 'bug', 'dragon', 'ghost', 'dark',
                       'steel', 'fairy')
    __directory = ""  # The global location of the code.
    __MAX_ID = 493  # Highest possible Pokemon ID.
    __regions = ('kanto', 'johto', 'hoenn', 'sinnoh')

    def __init__(self):
        self.__pokemon_list = []
        self.__pokemon_dictionary = {}
        self.__pokemon_type_dictionary = {}
        self.directory = os.path.dirname(os.path.realpath(__file__))
        for pkmn_t in self.__POKEMON_TYPES:
            self.__pokemon_type_dictionary[pkmn_t] = []
        self.__load_data()
        self.__load_extra()

    def __str__(self):
        return "\n".join(str(element) for element in self.__pokemon_list)

    def __contains__(self, pokemon):
        # Check for a Pokemon by ID or name.
        if isinstance(pokemon, int) or str(pokemon).isdigit():
            return self.pokemon_id_exists(int(pokemon))
        elif isinstance(pokemon, str):
            return self.__pokemon_dictionary.get(pokemon) is not None
        else:
            return self.pokemon_name_exists(pokemon.get_name())

    def __len__(self):
        return len(self.__pokemon_list)

    def get_pokemon_types(self):
        return [t for t in self.__POKEMON_TYPES]

    def get_pokemon_of_type(self, pkmn_type: str, single: bool = True):
        pkmns = self.__pokemon_type_dictionary.get(pkmn_type)
        if pkmns is None:
            return None
        return random.choice(pkmns) if single else pkmns

    def get_all(self):
        # Get all the Pokemon.
        return [pokemon for pokemon in self.__pokemon_list]
        # or... return self.__pokemon_list[:]
        # return a copy of self.__pokemon_list

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
        return [p for p in self.__pokemon_list if p.is_extra()]

    def get_light(self, threshold=0.4, all_pkmn=False):
        light = [pokemon.get_name() for pokemon in self.__pokemon_list
                 if pokemon.get_dark_threshold() > threshold]
        return light if all_pkmn else random.choice(light)

    def get_dark(self, threshold=0.6, all_pkmn=False):
        dark = [pokemon.get_name() for pokemon in self.__pokemon_list
                if pokemon.get_dark_threshold() < threshold]
        return dark if all_pkmn else random.choice(dark)

    def __get_region(self, region):
        # Helper method for getting all the Pokemon of a specified region.
        return [pokemon for pokemon in self.__pokemon_list
                if pokemon.get_region() == region and not pokemon.is_extra()]

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
        if isinstance(pokemon, Pokemon):
            return pokemon
        if not isinstance(pokemon, (int, str)):
            raise Exception("The parameter Pokemon must be of type integer" +
                            " or string.")
        if isinstance(pokemon, str):
            pokemon = pokemon.lower()
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
            raise Exception("The Pokemon ID must be between 1 and " +
                            str(self.__MAX_ID) + " inclusive.")
        # Subtract 1 to convert to 0 base indexing.
        return self.__pokemon_list[identifier - 1]

    def names_with_prefix(self, prefix):
        # Return Pokemon who's names begin with the specified prefix.
        return [pokemon for pokemon in self.__pokemon_list
                if str(pokemon.get_name()).startswith(prefix)]

    def names_with_infix(self, infix):
        # Return Pokemon who's names contains the specified infix.
        return [pokemon for pokemon in self.__pokemon_list
                if infix in str(pokemon.get_name())]

    def __load_data(self):
        # Load all the Pokemon data. This does not include the 'Extra' Pokemon.
        with open(self.directory + "/./Data/pokemon.txt", 'r') as data_file:
            # Load everything but the Pokemon from the 'Extra' folder.
            for i, line in enumerate(data_file):
                identifier = int(i) + 1
                pkmn_data = line.strip().split()
                name = pkmn_data[0]
                dark_threshold = pkmn_data[1]
                pkmn_type = pkmn_data[2]
                pkmn_type_snd = pkmn_data[3] if len(pkmn_data) >= 4 else ""
                identifier = '{:03}'.format(identifier)
                region = self.__determine_region(identifier)
                path = self.__determine_folder(identifier) + "/" + identifier\
                    + ".jpg"
                pokemon = Pokemon(identifier, name, region, path, pkmn_type,
                                  pkmn_type_snd, dark_threshold)
                self.__pokemon_type_dictionary[pkmn_type].append(pokemon)
                if pkmn_type_snd != '':
                    self.__pokemon_type_dictionary[pkmn_type_snd]\
                            .append(pokemon)
                self.__pokemon_list.append(pokemon)
                self.__pokemon_dictionary[pokemon.get_name()] = pokemon

    def __load_extra(self):
        """Load all the file names of the images in the Extra folder."""
        extra_dir = os.path.join(self.directory, "Images", "Extra")
        for file in os.listdir(extra_dir):
            name, ext = os.path.splitext(file.lower())
            if ext == '.jpg':
                path = os.path.join(extra_dir, file)
                father = self.__pokemon_dictionary.get(name.split("-")[0])
                if father is not None:
                    pokemon = Pokemon(None, name, father.get_region(),
                                      path, father.get_pkmn_type(),
                                      father.get_pkmn_type_secondary(),
                                      father.get_dark_threshold())
                else:
                    pokemon = Pokemon(None, name, None, path, None, None, None)
                if name in self.__pokemon_dictionary:
                    raise Exception("Duplicate names detected.\nThe name of "
                                    + "the file " + str(name) + ".jpg in the "
                                    + "folder 'Extra' must be changed.")
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
        # Determine which folder a Pokemon is from.
        suffix_dict = {"kanto": "I - Kanto",
                       "johto": "II - Johto",
                       "hoenn": "III - Hoenn",
                       "sinnoh": "IV - Sinnoh"}
        suffix = suffix_dict.get(self.__determine_region(identifier))
        return "{}/Images/Generation {}".format(self.directory, suffix)
