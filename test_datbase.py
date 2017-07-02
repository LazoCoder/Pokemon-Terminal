#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from collections import namedtuple
from database import Database

tuple_store = False
try:
    MAX_ID = Database.MAX_ID
    tuple_store = True
except AttributeError:
    MAX_ID = 493  # Old Database makes db.__MAX_ID private :-(

region_info = namedtuple('region_info', 'roman_number start end')
region_dict = {
    'kanto': region_info('I', 1, 151),
    'johto': region_info('II', 152, 251),
    'hoenn': region_info('III', 252, 386),
    'sinnoh': region_info('IV', 387, 493),
    'extra': region_info('', 0, 0)
}


def test_first_database():
    db = Database()
    print('{} items in first database.'.format(db))


def test_second_database():
    db = Database()
    print('{} items in second database.'.format(db))


def test_get_extras():
    db = Database()
    if tuple_store:
        assert db.get_region('extra'), "db.get_region('extra') returns no pokemon"
    else:
        assert db.get_extra(), 'db.get_extra() returns no pokemon'


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
    for name, info in region_dict.items():
        if name != 'extra':
            assert counts[name] == info.end - info.start + 1
            print('{}: {}'.format(name, counts[name]))
    assert MAX_ID == counts['all']
    # test the number of pokemon is the Database
    assert len(Database()) == 517  # counts['all'] + extras


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
    pokemon = db.get_region(region_name) if tuple_store else get_region(db, region_name)
    assert pokemon, 'No pokemon found in region: ' + region_name
    # test that region_name is in region_dict
    region_info = region_dict[region_name]
    delta = region_info.end - region_info.start
    fmt = 'Testing {}({} vs. {}): {}'
    print(fmt.format(region_name, len(pokemon), delta + 1, region_info))
    # test the number of pokemon returned by db.get_region()
    assert len(pokemon) == delta + 1


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
    pokemon = db.get_region(region_name) if tuple_store else get_region(db, region_name)
    assert pokemon, 'No pokemon found in region: ' + region_name
    # test that region_name is in region_dict
    region_info = region_dict[region_name]
    delta = region_info.end - region_info.start
    fmt = 'Testing {}({} vs. {}): {}'
    print(fmt.format(region_name, len(pokemon), delta + 1, region_info))
    if region_name != 'extra':
        # test db.get_pokemon(id)
        middle_pokemon = db.get_pokemon(region_info.start + (delta // 2))
        assert middle_pokemon in pokemon
        # test db.get_pokemon(name)
        name = middle_pokemon.name if tuple_store else middle_pokemon.get_name()
        assert db.get_pokemon(name) in pokemon
        # test the case insensivity of db.get_pokemon(name)
        assert db.get_pokemon(name.upper()) in pokemon


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


def test_len():
    db = Database()
    len_extra = len(db.get_region('extra') if tuple_store else db.get_extra())
    assert len(db) == MAX_ID + len_extra


def _test_region(region_name):
    db = Database()
    region_name = (region_name or 'extra').lower()
    # Database unfortunately makes db.__get_region() private :-(
    func = {
        "kanto": db.get_kanto,
        "johto": db.get_johto,
        "hoenn": db.get_hoenn,
        "sinnoh": db.get_sinnoh,
        "extra": db.get_extra
    }[region_name]
    pokemon_list = func()
    region_record = region_dict[region_name]
    start = region_record.start
    end = len(db) if region_name == "extra" else region_record.end
    # make sure there are no missing pokemon
    assert len(pokemon_list) == end - start + 1
    if region_name == "extra":
        return
    # make sure that all pokemon.id are in the ID range
    assert all([start <= int(p.get_id()) <= end for p in pokemon_list])


def _ts_test_region(region_name):
    db = Database()
    pokemon_list = db.get_region(region_name)
    region_record = region_dict[region_name]
    start = region_record.start
    end = len(db) if region_name == "extra" else region_record.end
    # make sure there are no missing pokemon
    assert len(pokemon_list) == end - start + 1
    if region_name == "extra":
        return
    # make sure that all pokemon.id are in the ID range
    assert all([start <= p.id <= end for p in pokemon_list])

    
def test_regions_two():
    for region_name in region_dict:
        if tuple_store:
            _ts_test_region(region_name)
        else:
            _test_region(region_name)
