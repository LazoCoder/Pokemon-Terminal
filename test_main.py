#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from database import Database
from filters import Filter
import filters
from main import main
from test_utils import region_dict
import random

db = Database()
print(len(db))


def test_extra(capsys):
    main(['-e'])
    # TODO: Assertion based on number of files on ./Extras
    assert str(random.choice(Filter.filtered_list)).startswith('---')


def test_region_names(capsys):
    try:
        main(['-r', 'wrong_region'])
    except SystemExit:
        pass  # It's supposed to crash.
    err: str = capsys.readouterr()[1].strip()
    assert err.endswith("(choose from 'kanto', 'johto', 'hoenn', 'sinnoh')")


def region_test(capsys, region_name):
    regFilter = filters.RegionFilter()
    noExtras = filters.NonExtrasFilter()
    # matrix test of first pokemon name and last pokemon name from all regions
    for name, region_info in region_dict.items():
        filtered = [p for p in Filter.POKEMON_LIST
                    if regFilter.matches(p, name) and noExtras.matches(p)]
        assert len(filtered) == region_info.size
        assert random.choice(filtered).get_region() == name
        assert filtered[0].get_id() == ('%03d' % (region_info.start))
        assert filtered[-1].get_id() == ('%03d' % (region_info.end))
        assert filtered[0].get_name() == region_info.first
        assert filtered[-1].get_name() == region_info.last


if __name__ == '__main__':
    # Test runner: Runs all functions whose name begins with `test_`
    # locals() changes when trying to do this without the list comprehension!!!
    name_funcs = [(n, f) for n, f in locals().items() if n.startswith('test_')]
    for name, func in name_funcs:
        if callable(func):
            func()
        else:
            print(name + ' is not callable()!')
