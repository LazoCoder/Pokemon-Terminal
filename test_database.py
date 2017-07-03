#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from collections import Counter, namedtuple
from database import Database
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAX_ID = 493

region_info = namedtuple('region_info', 'start end')
region_dict = {
    'kanto': region_info(1, 151),
    'johto': region_info(152, 251),
    'hoenn': region_info(252, 386),
    'sinnoh': region_info(387, 493),
}

extra_counts = None  # Set below after make_extra_counts() is defined


def _pokemon_id_to_region(pokemon_id):
    """Rewrite of Database.__determine_region() avoids sharing implementations
       between production code and test code."""
    for region_name, region_info in region_dict.items():
        if region_info.start <= pokemon_id <= region_info.end:
            return region_name
    assert False, '{} is an invalid region'.format(pokemon_id)


def make_extra_counts(filename='pokemon.txt'):
    """Test that correct regions are used in load_all_pokemon.load_extras().
       Currently generates the dict: {'sinnoh': 14, 'hoenn': 9, 'johto': 1}"""
    with open(os.path.join(SCRIPT_DIR, 'Data', filename)) as in_file:
        pokemon_names = tuple([line.split()[0] for line in in_file])
    filenames = os.listdir(os.path.join(SCRIPT_DIR, 'Images', 'Extra'))
    father_names = (filename.split('-')[0] for filename in filenames)
    father_ids = (pokemon_names.index(name) for name in father_names)
    father_regions = (_pokemon_id_to_region(id) for id in father_ids)
    return dict(Counter(father_regions))


extra_counts = make_extra_counts()


def test_first_database():
    print('{} items in first database.'.format(Database()))


def test_second_database():
    print('{} items in second database.'.format(Database()))


def test_len():
    db = Database()
    assert len(db) == MAX_ID + len(db.get_extra())


def test_extra_counts():
    assert len(Database()) == MAX_ID + sum(extra_counts.values())


def test_get_extras():
    db = Database()
    assert db.get_extra(), 'db.get_extra() returns no pokemon'
    assert db.get_extra() == sum(extra_counts.values())


def test_region_dict():
    # test if region_dict counts match wikipedia
    print('From https://en.wikipedia.org/wiki/Pok%C3%A9mon#Generation_1 ...')
    counts = {
        'kanto': 151,
        'johto': 100,
        'hoenn': 135,
        'sinnoh': 107,
        'all': 493
    }
    region_counts = (counts[r] for r in 'kanto johto hoenn sinnoh'.split())
    assert counts['all'] == sum(region_counts) == MAX_ID
    for name, info in region_dict.items():
        assert counts[name] == info.end - info.start + 1
        print('{}: {}'.format(name, counts[name]))


def get_region(db, region_name):
    """Database unfortunately makes db.__get_region() private :-("""
    func = {
        'kanto': db.get_kanto,
        'johto': db.get_johto,
        'hoenn': db.get_hoenn,
        'sinnoh': db.get_sinnoh,
        'extra': db.get_extra
    }[region_name]
    return func()


def region_length_test(region_name):
    db = Database()
    # test db.get_region()
    pokemon = db.get_region(region_name) if tuple_store else get_region(
        db, region_name)
    assert pokemon, 'No pokemon found in region: ' + region_name
    # test that region_name is in region_dict
    region_info = region_dict[region_name]
    extra_count = extra_counts.get(region_name, 0)
    expected_len = region_info.end - region_info.start + 1 + extra_count
    fmt = 'Testing {}({} vs. {}): {}'
    print(fmt.format(region_name, len(pokemon), expected_len, region_info))
    # test the number of pokemon returned by db.get_region()
    assert len(pokemon) == expected_len


def test_kanto_length():
    region_length_test('kanto')


def test_johto_length():
    region_length_test('johto')


def test_hoenn_length():
    region_length_test('hoenn')


def test_sinnoh_length():
    region_length_test('sinnoh')


def region_test(region_name):
    db = Database()
    # test db.get_region()
    pokemon = db.get_region(region_name) if tuple_store else get_region(
        db, region_name)
    assert pokemon, 'No pokemon found in region: ' + region_name
    # test that region_name is in region_dict
    region_info = region_dict[region_name]
    delta = region_info.end - region_info.start
    fmt = 'Testing {}({} vs. {}): {}'
    print(fmt.format(region_name, len(pokemon), delta + 1, region_info))
    # test db.get_pokemon(id)
    middle_pokemon = db.get_pokemon(region_info.start + (delta // 2))
    assert middle_pokemon in pokemon
    # test db.get_pokemon(name)
    name = middle_pokemon.name if tuple_store else middle_pokemon.get_name()
    assert db.get_pokemon(name) in pokemon
    # test the case insensivity of db.get_pokemon(name)
    # assert db.get_pokemon(name.upper()) in pokemon  # !!! FixMe !!!


def test_kanto():
    region_test('kanto')


def test_johto():
    region_test('johto')


def test_hoenn():
    region_test('hoenn')


def test_sinnoh():
    region_test('sinnoh')


def test_regions():
    for region_name in region_dict:
        region_test(region_name)


def _test_region(region_name):
    db = Database()
    # Database unfortunately makes db.__get_region() private :-(
    func = {
        "kanto": db.get_kanto,
        "johto": db.get_johto,
        "hoenn": db.get_hoenn,
        "sinnoh": db.get_sinnoh,
    }[region_name]
    pokemon_list = func()
    region_record = region_dict[region_name]
    # make sure there are no missing pokemon
    start = region_record.start
    end = region_record.end
    extra_count = extra_counts.get(region_name, 0)
    assert len(pokemon_list) == end - start + 1 + extra_count
    # make sure that all pokemon.id == '---' or are in the ID range
    assert all([start <= int(p.get_id()) <= end for p in pokemon_list if p.get_id() != '---'])


def test_regions_two():
    for region_name in region_dict:
        _test_region(region_name)
