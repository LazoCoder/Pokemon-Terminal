#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from database import Database
from test_database import make_extra_counts

print('From https://en.wikipedia.org/wiki/Pok%C3%A9mon#Generation_1 ...')
counts = {'kanto': 151, 'johto': 100, 'hoenn': 135, 'sinnoh': 107, 'all': 493}
for region_name, extra_count in make_extra_counts().items():
    counts[region_name] += extra_count  # add the extras to the wikipedia counts


def test_extra_length():  # fails: 0 record
    assert Database().get_extra()  # Fails: returns zero pokemon!'


def test_kanto_length(region_name='kanto'):
    region_name = 'kanto'
    assert len(Database().get_kanto()) == counts[region_name]


def test_johto_length(region_name='johto'):
    assert len(Database().get_johto()) == counts[region_name]


def test_hoenn_length(region_name='hoenn'):
    assert len(Database().get_hoenn()) == counts[region_name]


def test_sinnoh_length(region_name='sinnoh'):
    assert len(Database().get_sinnoh()) == counts[region_name]
