#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

"""These are general utilities for testing Pokemon Terminal. The data and
   functions in this file can be used by other `test_*.py` scripts but they
   should not be imported into or copied into normal scripts in the project.
   This approach will help us to steer clear of assumption bias and avoid
   shared code between dev and test."""

import os
from collections import Counter, namedtuple

import pokemonterminal


MAX_ID = 719  # Also total pokemon
SCRIPT_DIR = os.path.dirname(os.path.realpath(pokemonterminal.__file__))

region_info = namedtuple("region_info", "start end first last size")
region_dict = {
    "kanto": region_info(1, 151, "Bulbasaur", "Mew", 151),
    "johto": region_info(152, 251, "Chikorita", "Celebi", 100),
    "hoenn": region_info(252, 386, "Treecko", "Deoxys", 135),
    "sinnoh": region_info(387, 493, "Turtwig", "Arceus", 107),
    "unova": region_info(494, 649, "Victini", "Genesect", 156),
    "kalos": region_info(650, 719, "Chespin", "Diancie", 70),
}


def expected_len(region_name):
    """Utility function for knowing the standard pokemon population."""
    if region_name == "all":
        return MAX_ID
    elif region_name == "extra":
        return sum(make_extra_counts().values())  # 24
    region_info = region_dict[region_name]
    return region_info.end - region_info.start + 1


def get_region(db, region_name):
    """Database unfortunately makes db.__get_region() private :-("""
    func = {
        "kanto": db.get_kanto,
        "johto": db.get_johto,
        "hoenn": db.get_hoenn,
        "sinnoh": db.get_sinnoh,
        "unova": db.get_unova,
        "kalos": db.get_kalos,
        "extra": db.get_extra,
        "all": db.get_all,
    }[region_name]
    return func()


def _pokemon_id_to_region(pokemon_id):
    """Rewrite of Database.__determine_region() avoids sharing implementations
       between production code and test code."""
    for region_name, region_info in region_dict.items():
        if region_info.start <= pokemon_id <= region_info.end:
            return region_name
    assert False, "{} is an invalid region".format(pokemon_id)


def make_extra_counts(filename="pokemon.txt"):
    """Test that correct regions are used in load_all_pokemon.load_extras().
       Currently generates the dict: {'sinnoh': 14, 'hoenn': 9, 'johto': 1}"""
    with open(os.path.join(SCRIPT_DIR, "Data", filename)) as in_file:
        pokemon_names = tuple([line.split()[0] for line in in_file])
    filenames = os.listdir(os.path.join(SCRIPT_DIR, "Images", "Extra"))
    father_names = (filename.split("-")[0] for filename in filenames)
    father_ids = (pokemon_names.index(name) for name in father_names)
    father_regions = (_pokemon_id_to_region(id) for id in father_ids)
    return dict(Counter(father_regions))
