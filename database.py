#!/usr/bin/env python3

# The Database object is a container for all the supported Pokemon.

import random
from load_all_pokemon import as_str, load_all_pokemon, region_dict


class Database:
    MAX_ID = 493  # Highest possible Pokemon ID.

    def __init__(self, pokemon_list=None):
        self.pokemon_list = pokemon_list or load_all_pokemon()
        assert self.pokemon_list, 'Failed to load the Pokemon list!!'
        self.pokemon_dict = {p.name: p for p in self.pokemon_list}
        assert len(self.pokemon_list) == len(self.pokemon_dict), 'DuplicateErr'

    def __str__(self):
        return '\n'.join(as_str(p) for p in self.pokemon_list)

    def __contains__(self, pokemon):
        """Check for the presence of a Pokemon by ID or name."""
        return self.id_exists(pokemon) or self.name_exists(pokemon)

    def __len__(self):
        return len(self.pokemon_list)

    @property
    def all_pokemon(self):
        """Get all the Pokemon. Caution: returns generator expression"""
        return (p for p in self.pokemon_list)

    def get_light_pokemon(self, threshold=0.4):
        return (p for p in self.pokemon_list if p.threshold > threshold)

    def get_dark_pokemon(self, threshold=0.6):
        return (p for p in self.pokemon_list if p.threshold < threshold)

    def get_region(self, region):
        """Helper method for getting all the Pokemon of a specified region"""
        assert region in region_dict, 'Invalid region: ' + region
        return (p for p in self.pokemon_list if p.region == region)

    @property
    def random_pokemon(self):
        """Select a random Pokemon from the database."""
        return random.choice(self.pokemon_list)

    def id_exists(self, identifier):
        """Check for Pokemon by ID."""
        try:
            return 0 < int(float(identifier)) <= self.MAX_ID
        except (TypeError, ValueError):
            return False

    def name_exists(self, name):
        """Check for Pokemon by Name."""
        return str(name).lower() in self.pokemon_dict

    def get_pokemon(self, pokemon):
        """Get a Pokemon by name or ID."""
        if self.id_exists(pokemon):
            return self.get_pokemon_by_id(pokemon)
        else:
            return self.get_pokemon_by_name(pokemon)

    def get_pokemon_by_id(self, identifier):
        """Get a Pokemon by its ID.  Will not work for extras (ID==0)."""
        try:
            i = int(float(
                identifier)) - 1  # Minus 1 to convert to 0 based indexing
        except (TypeError, ValueError):
            fmt = "The Pokemon ID ({}) must be a number."
            raise TypeError(fmt.format(identifier))
        if 0 < i <= self.MAX_ID:
            return self.pokemon_list[i]
        else:
            fmt = "The Pokemon ID ({}) must be between 1 and {} inclusive."
            raise Exception(fmt.format(identifier, self.MAX_ID))

    def get_pokemon_by_name(self, name):
        """Get a Pokemon by its name."""
        pokemon = self.pokemon_dict.get(str(name).lower())
        if pokemon:
            return pokemon
        if not isinstance(name, str):
            raise TypeError("The type of name must be a string.")
        else:
            raise Exception("No such Pokemon in the database.")

    def get_pokemon_by_name_infix(self, infix):
        """Return Pokemon whose name contains the specified infix."""
        return (pkmn for pkmn in self.pokemon_list if infix in pkmn.name)

    def get_pokemon_by_name_prefix(self, prefix):
        """Return Pokemon whose name begin with the specified prefix."""
        return (p for p in self.pokemon_list if p.name.startswith(prefix))

    def get_pokemon_by_type(self, type_name):
        return (p for p in self.pokemon_list if type_name in p.types)

    def get_pokemon_by_main_type(self, type_name):
        return (p for p in self.pokemon_list if type_name == p.types[0])

    def get_pokemon_by_subtype(self, type_name):
        return (p for p in self.pokemon_list if type_name == p.types[1])

    @property
    def main_types(self):
        return tuple(
            sorted(set(p.types[0] for p in self.pokemon_list if p.types[0])))

    @property
    def subtypes(self):
        return tuple(
            sorted(set(p.types[1] for p in self.pokemon_list if p.types[1])))


if __name__ == '__main__':
    db = Database()
    print(len(db))
    assert len(db) == 518
    assert db.name_exists('chimecho'.upper())
    assert db.id_exists('358.742')
    assert db.id_exists(358.742)
    print(db.get_pokemon_by_name('chimecho'.upper())._asdict())
    print(db.get_pokemon_by_id('358.742'))
    print(db.get_pokemon_by_id(358.742))
    print()
    print(db.get_pokemon('chimecho'.upper()))
    print(db.get_pokemon('358.742'))
    print(db.get_pokemon(358.742))
    print()
    for _ in range(5):  # test saveral ramdom pokemon
        pokemon = db.random_pokemon
        print(pokemon)
        assert pokemon.name in db
        assert pokemon == db.get_pokemon_by_name(pokemon.name)
        assert pokemon in db.get_pokemon_by_name_prefix(pokemon.name[:-1])
        assert pokemon in db.get_pokemon_by_name_infix(pokemon.name[1:-1])
    print()
    print('main_types:', db.main_types)
    print('  subtypes:', db.subtypes)
    print(tuple(set(db.main_types) - set(db.subtypes)))
    print(tuple(set(db.subtypes) - set(db.main_types)))
    print(len(list(db.get_pokemon_by_type('dragon'))))
    print(len(list(db.get_pokemon_by_main_type('dragon'))))
    print(len(list(db.get_pokemon_by_subtype('dragon'))))
    # print(db)
