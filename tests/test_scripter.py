#!/usr/bin/env python3

# To run use python3 -m pytest --capture=sys

import os

from pokemonterminal.adapter import available_terminals, base
from tests.test_utils import SCRIPT_DIR


def test_available_terminals():
    assert available_terminals, 'No available_terminals found.'
    terminal_names = [terminal.__name__ for terminal in available_terminals]
    non_terminals = ['NullAdapter', '__init__']
    assert all(terminal not in terminal_names for terminal in non_terminals)
    terminals_dir = os.path.join(SCRIPT_DIR, 'adapter', 'implementations')
    assert os.path.isdir(terminals_dir), 'Not found: ' + terminals_dir
    for filename in os.listdir(terminals_dir):
        terminal, ext = os.path.splitext(filename)
        if ext.lower() == '.py':
            assert terminal in (terminal_names + non_terminals), terminal


def test_adapter_methods():
    for terminal in available_terminals + [base.TerminalAdapterInterface]:
        assert callable(terminal.clear)
        assert callable(terminal.is_available)
        assert callable(terminal.set_image_file_path)
        assert callable(terminal.get_image_file_number)


if __name__ == '__main__':
    test_available_terminals()
