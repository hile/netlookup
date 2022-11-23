"""
Unit tests for CLI command 'netlookup substract'
"""

import pytest

from netlookup.bin.netlookup import main


def test_commands_subtract_no_args(monkeypatch):
    """
    Test initializing subtract command
    """
    test_args = ['netlookup', 'subtract']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 2


def test_commands_subtract_substracted_no_subnets(monkeypatch):
    """
    Test initializing subtract command
    """
    test_args = ['netlookup', 'subtract', '-n', '192.168.0.0/33']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1


def test_commands_subtract_invalid_subnets(monkeypatch):
    """
    Test initializing subtract command
    """
    test_args = [
        'netlookup', 'subtract',
        '-n', '192.168.0.0/29',
        '192.168.0.0/33'
    ]
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1


def test_commands_subtract_invalid_substracted_subnets(monkeypatch):
    """
    Test initializing subtract command
    """
    test_args = [
        'netlookup', 'subtract',
        '-n', '192.168.0.0/33',
        '192.168.0.0/24'
    ]
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1


def test_commands_subtract_valid_substracted_subnets(monkeypatch):
    """
    Test initializing subtract command
    """
    test_args = [
        'netlookup', 'subtract',
        '-n', '192.168.0.0/29,192.168.1.0/29',
        '192.168.0.0/24', '10.0.0.0/8'
    ]
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
