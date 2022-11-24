"""
Unit tests for netlookup.bin.netlookup module
"""
import sys

import pytest

from netlookup.bin. netlookup import main


def test_cli_netlookup_help(monkeypatch):
    """
    Test running 'netlookup --help'
    """
    monkeypatch.setattr(sys, 'argv', ['netlookup', '--help'])
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0


def test_cli_netlookup_no_args(monkeypatch):
    """
    Test running 'netlookup' with no arguments
    """
    monkeypatch.setattr(sys, 'argv', ['netlookup'])
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1
