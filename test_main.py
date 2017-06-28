#!/usr/bin/env python -m pytest --capture=sys

from database import Database
from main import main


def test_no_args(capsys):
    main([__file__])
    out, err = capsys.readouterr()
    assert out.startswith("No command line arguments specified.")


def test_len():
    __MAX_ID = 493
    db = Database()
    assert len(db) == __MAX_ID + len(db.get_extra())


def test_three_args(capsys):
    main([__file__, 1, 2, 3])
    out, err = capsys.readouterr()
    assert out.startswith("Invalid number of arguments.")
