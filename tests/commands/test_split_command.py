"""
Unit tests for CLI command 'netlookup split'
"""

import pytest

from netlookup.bin.netlookup import main


def test_commands_split_no_args(monkeypatch):
    """
    Test initializing split command
    """
    test_args = ['netlookup', 'split']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.type == SystemExit
    assert exit_status.value.code == 1


def test_commands_split_run_with_subnets_invalid_mask(monkeypatch):
    """
    Test initializing split with subnets
    """
    test_args = ['netlookup', 'split', '--mask', '23', '192.168.0.0/24']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0


def test_commands_split_run_with_subnets_unsplittable(monkeypatch):
    """
    Test initializing split with subnets
    """
    test_args = ['netlookup', 'split', '192.168.0.0/32']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0


def test_commands_split_run_with_subnets_default_split(monkeypatch):
    """
    Test initializing split with subnets
    """
    test_args = ['netlookup', 'split', '192.168.0.0/24']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0


def test_commands_split_run_with_subnets_explicit_mask(monkeypatch):
    """
    Test initializing split with subnets
    """
    test_args = ['netlookup', 'split', '--mask', '26', '192.168.0.0/24']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
