#!/usr/bin/env python3

# To run the tests, use: python3 -m pytest --capture=sys

from database import Database
from main import main
from test_utils import region_dict

db = Database()
print(len(db))


def test_no_args(capsys):
    main([__file__])
    out, err = capsys.readouterr()
    assert out.startswith("No command line arguments specified.")


def test_three_args(capsys):
    main([__file__, 1, 2, 3])
    out, err = capsys.readouterr()
    assert out.startswith("Invalid number of arguments.")


def test_two_letters(capsys):
    main([__file__, 'bu'])
    out, err = capsys.readouterr()
    assert 'Butterfree' in out
    # prefix search only
    main([__file__, 'ut'])
    out, err = capsys.readouterr()
    assert 'butterfree' not in out.lower()


def test_extra(capsys):
    main([__file__, 'extra'])
    out, err = capsys.readouterr()
    assert out.count('Castform') == 3, out  # issue #89
    assert 'turtwig' not in out.lower()


def test_region_names(capsys):
    main([__file__, 'regions'])
    out, err = capsys.readouterr()
    for region_name in region_dict:
        assert region_name in out


def test_help(capsys):
    main([__file__, 'help'])
    out, err = capsys.readouterr()
    assert 'Usage:' in out
    main([__file__, '-h'])
    out2, err = capsys.readouterr()
    assert out2 == out


def region_test(capsys, region_name):
    main([__file__, region_name])
    out, err = capsys.readouterr()
    # matrix test of first pokemon name and last pokemon name from all regions
    for name, region_info in region_dict.items():
        if name == 'extra':
            continue
        assert (region_info.first in out) == (name == region_name)
        assert (region_info.last in out) == (name == region_name)


def test_kanto(capsys):
    region_test(capsys, 'kanto')


def test_johto(capsys):
    region_test(capsys, 'johto')


def test_hoenn(capsys):
    region_test(capsys, 'hoenn')


def test_sinnoh(capsys):
    region_test(capsys, 'sinnoh')


def test_all(capsys):
    main([__file__, 'all'])
    out, err = capsys.readouterr()
    for region_info in region_dict.values():
        assert (region_info.first or '') in out  # convert None --> ''
        assert (region_info.last or '') in out   # convert None --> ''


def test_question_mark(capsys):
    main([__file__, '?'])
    out, err = capsys.readouterr()
    assert 'deprecated' in out


if __name__ == '__main__':
    # Test runner: Runs all functions whose name begins with `test_`
    # locals() changes when trying to do this without the list comprehension!!!
    name_funcs = [(n, f) for n, f in locals().items() if n.startswith('test_')]
    for name, func in name_funcs:
        if callable(func):
            func()
        else:
            print(name + ' is not callable()!')
