#!/usr/bin/env python3

import collections
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'Data')
IMAGES_DIR = os.path.join(SCRIPT_DIR, 'Images')
EXTRA_DIR = os.path.join(IMAGES_DIR, 'Extra')

# *********************
Pokemon = collections.namedtuple('Pokemon',
                                 'id name region types threshold path')


def is_extra(pokemon):
    return not pokemon.id


def as_str(pokemon):
    id = '{:03}'.format(pokemon.id) if pokemon.id else '---'
    return '{} {name} at {path}'.format(id, **pokemon._asdict())


# *********************
Region = collections.namedtuple('Region', 'start end dir_name')
region_dict = {
    'kanto': Region(1, 151, 'Generation I - Kanto'),
    'johto': Region(152, 251, 'Generation II - Johto'),
    'hoenn': Region(252, 386, 'Generation III - Hoenn'),
    'sinnoh': Region(387, 493, 'Generation IV - Sinnoh'),
    'extra': Region(494, 100000, '')
}


def region_name_by_id(id):
    if not id:
        return 'extra'
    for name, region in region_dict.items():
        if region.start <= id <= region.end:
            return name
    assert False, 'region_by_id({})'.format(id)


# *********************
def make_a_pokemon(i, line):
    id = i + 1
    line = line.strip().split()
    name, threshold, main_type = line[:3]
    types = (main_type, line[3]) if len(line) > 3 else (main_type, )
    region = region_name_by_id(id)
    dir_name = region_dict[region].dir_name
    path = os.path.join(IMAGES_DIR, dir_name, '{:03}.jpg'.format(id))
    return Pokemon(id, name.title(), region, types, threshold, path)


def load_pokemon(filename='p.txt'):
    """Load everything but the Pokemon from the 'Extra' folder"""
    with open(os.path.join(SCRIPT_DIR, filename)) as in_file:
        return [make_a_pokemon(i, line) for i, line in enumerate(in_file)]


def make_an_extra_pokemon(filename, in_ext='.png'):
    root, ext = os.path.splitext(filename)
    if ext.lower() == in_ext:
        path = os.path.join(EXTRA_DIR, filename)
        pokemon = Pokemon(0, root.title(), None, (), 5, path)
        return pokemon
    assert False, 'Bad file extention: {} != {}'.format(ext, in_ext)


def load_extra():
    """Load all the file names of the images in the Extra folder."""
    filenames = os.listdir(EXTRA_DIR)
    return [make_an_extra_pokemon(filename) for filename in filenames]


def load_all_pokemon():
    return load_pokemon() + load_extra()


if __name__ == '__main__':
    pokemon_list = load_all_pokemon()
    pokemon_dict = {pokemon.name: pokemon for pokemon in pokemon_list}
    print(len(pokemon_list), len(set(pokemon_list)), len(pokemon_dict))
    for i in (0, -1):
        pokemon = pokemon_list[i]
        print(is_extra(pokemon), as_str(pokemon))
        print(pokemon)
