#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from database import Database, Pokemon
from load_all_pokemon import load_all_pokemon
from test_utils import expected_len, MAX_ID


def compare_pokemon(a, b):
    assert isinstance(a, Pokemon)
    assert isinstance(b, Pokemon)
    assert a.get_id() == b.get_id()
    assert a.get_name() == b.get_name()
    assert a.get_region() == b.get_region()
    assert a.get_path() == b.get_path()
    assert a.get_dark_threshold() == b.get_dark_threshold()
    assert a.get_pkmn_type() == b.get_pkmn_type()
    assert a.get_pkmn_type_secondary() == b.get_pkmn_type_secondary()
    # print(a.get_name())


def test_len():
    assert len(Database()) == len(load_all_pokemon()) == MAX_ID + expected_len('extra')


def test_lists():
    db = Database()
    load_list = load_all_pokemon()
    for db_p, load_p in zip(db.get_all(), load_list):
        assert str(db_p) == str(load_p)
        compare_pokemon(db_p, load_p)
        # db_p != load_p but the hidden __attributes stifle complete testing
        # assert db_p == load_p, '\n{}\n{}'.format(db_p, load_p)
    # the lists are not identical but hidden __attributes stifle complete tests
    # assert db.get_all() == load_list


if __name__ == '__main__':
    # Test runner: Runs all functions whose name begins with `test_`
    # locals() changes when trying to do this without the list comprehension!!!
    name_funcs = [(n, f) for n, f in locals().items() if n.startswith('test_')]
    for name, func in name_funcs:
        if callable(func):
            func()
        else:
            print(name + ' is not callable()!')
