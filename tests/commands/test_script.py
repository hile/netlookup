"""
Unit tests for CLI command 'netlookup' base class
"""

import pytest

from netlookup.bin.netlookup import main


def test_commands_main_no_args(monkeypatch):
    """
    Test initializing command 'netlookup' without arguments
    """
    test_args = ['netlookup']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1


def test_commands_main_help(monkeypatch):
    """
    Test initializing command 'netlookup --help'
    """
    test_args = ['netlookup', '--help']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
