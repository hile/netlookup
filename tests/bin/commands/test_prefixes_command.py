"""
Unit tests for CLI command 'netlookup prefixes'
"""

import pytest

from netlookup.bin.netlookup import main
from netlookup.network import NetworkError


def mock_fail_vendor_update():
    """
    Method to mock error updating vendor data
    """
    raise NetworkError('Mock failed update')


def test_commands_prefixes_no_args(monkeypatch):
    """
    Test initializing prefixes command
    """
    test_args = ['netlookup', 'prefixes']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1


def test_commands_prefixes_update_cache(monkeypatch):
    """
    Test updating prefixes cache
    """
    test_args = ['netlookup', 'prefixes', '--update']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0


def test_commands_prefixes_lookup_known_address(monkeypatch):
    """
    Test lookup for address in prefixes cache
    """
    test_args = ['netlookup', 'prefixes', '8.34.223.255']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0


def test_commands_prefixes_lookup_internal_address(monkeypatch):
    """
    Test lookup for address not in prefixes cache
    """
    test_args = ['netlookup', 'prefixes', '192.168.0.1']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0


def test_commands_prefixes_lookup_invalid_address(monkeypatch):
    """
    Test lookup for invalid address
    """
    test_args = ['netlookup', 'prefixes', 'foobar']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
