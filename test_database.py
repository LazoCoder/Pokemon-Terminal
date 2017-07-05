#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from database import Database
from test_utils import region_dict, get_region, make_extra_counts, MAX_ID


def test_first_database():
    print('{} items in first database.'.format(len(Database())))


def test_second_database():
    print('{} items in second database.'.format(len(Database())))


def test_len():
    db = Database()
    assert len(db) == MAX_ID + len(db.get_extra())
    assert len(db.get_all()) == MAX_ID + len(db.get_extra())


def test_extra_counts():
    assert len(Database()) == MAX_ID + sum(make_extra_counts().values())


def test_get_extras():
    db = Database()
    assert db.get_extra(), 'db.get_extra() returns no pokemon'
    assert len(db.get_extra()) == sum(make_extra_counts().values())


def region_length_test(region_name):
    db = Database()
    # test db.get_region()
    pokemon = get_region(db, region_name)
    assert pokemon, 'No pokemon found in region: ' + region_name
    # test that region_name is in region_dict
    region_info = region_dict[region_name]
    # extra_count = extra_counts.get(region_name, 0)
    expected_len = region_info.end - region_info.start + 1  # + extra_count
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
    pokemon = get_region(db, region_name)
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
    name = middle_pokemon.get_name()
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
    # extra_count = extra_counts.get(region_name, 0)
    assert len(pokemon_list) == end - start + 1  # + extra_count
    # make sure that all pokemon.id == '---' or are in the ID range
    assert all([start <= int(p.get_id()) <= end for p in pokemon_list if p.get_id() != '---'])


def test_regions_two():
    for region_name in region_dict:
        _test_region(region_name)


def test_ids():
    db = Database()
    numbered_ids = [p.get_id() for p in db.get_all() if p.get_id() != '---']
    # test that all that are not --- are unique (no duplicate ids)
    assert len(set(numbered_ids)) == len(numbered_ids) == MAX_ID
    for id_str in numbered_ids:
        assert len(id_str) == 3
        assert isinstance(id_str, str)
        assert 1 <= int(id_str) <= MAX_ID


def test_thresholds():
    db = Database()
    assert all(isinstance(p.get_dark_threshold(), float) for p in db.get_all())
