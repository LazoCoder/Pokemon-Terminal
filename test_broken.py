#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from database import Database
from test_utils import expected_len


def test_extra_length(region_name='extra'):
    assert len(Database().get_extra()) == expected_len(region_name)


def test_kanto_length(region_name='kanto'):
    assert len(Database().get_kanto()) == expected_len(region_name)


def test_johto_length(region_name='johto'):
    assert len(Database().get_johto()) == expected_len(region_name)


def test_hoenn_length(region_name='hoenn'):
    assert len(Database().get_hoenn()) == expected_len(region_name)


def test_sinnoh_length(region_name='sinnoh'):
    assert len(Database().get_sinnoh()) == expected_len(region_name)


def test_all_length(region_name='all'):
    expected = expected_len(region_name) + expected_len('extra')
    assert len(Database().get_all()) == expected
