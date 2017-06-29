#!/usr/bin/env python -m pytest --capture=sys

from collections import namedtuple
from database import Database
from main import main

region_record = namedtuple('region_record', 'roman_number start end')
region_dict = {"kanto": region_record("I", 1, 151),
               "johto": region_record("II", 152, 251),
               "hoenn": region_record("III", 252, 386),
               "sinnoh": region_record("IV", 387, 493),
               "extra": region_record("", 494, 100000)}


def test_no_args(capsys):
    main([__file__])
    out, err = capsys.readouterr()
    assert out.startswith("No command line arguments specified.")


def test_len():
    __MAX_ID = 493
    db = Database()
    assert len(db) == __MAX_ID + len(db.get_extra())


def _test_region(region_name):
    region_name = (region_name or 'extra').lower()
    db = Database()
    # Database unfortunately makes db.__get_region() private :-(
    func = {"kanto": db.get_kanto,
            "johto": db.get_johto,
            "hoenn": db.get_hoenn,
            "sinnoh": db.get_sinnoh,
            "extra": db.get_extra}[region_name]
    pokemon_list = func()
    region_record = region_dict[region_name]
    start = region_record.start
    end = len(db) if region_name == "extra" else region_record.end
    # make sure there are no missing pokemon
    assert len(pokemon_list) == end - start + 1
    # make sure that all pokemon.id are in the ID range
    assert all([start < int(p.id) < end for p in __pokemon_list])


def test_regions():
    for region_name in region_dict:
        _test_region(region_name)


def test_three_args(capsys):
    main([__file__, 1, 2, 3])
    out, err = capsys.readouterr()
    assert out.startswith("Invalid number of arguments.")
