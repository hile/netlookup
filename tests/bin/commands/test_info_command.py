"""
Unit tests for CLI command 'netlookup info'
"""

import pytest

from netlookup.bin.netlookup import main


def mock_message_callback(*args):
    """
    Test message callback is called
    """
    print(*args)


def test_commands_info_no_args(monkeypatch):
    """
    Test initializing Info command parse_args
    """
    test_args = ['netlookup', 'info']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.type == SystemExit
    assert exit_status.value.code == 1


def test_commands_info_run_with_subnet(monkeypatch):
    """
    Test initializing info with subnets
    """
    test_args = ['netlookup', 'info', '192.168.0.0/24', '192.168.0.255/32']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0


def test_commands_info_run_invalid_subnets(monkeypatch):
    """
    Test initializing info with invalid subnets
    """
    test_args = ['netlookup', 'info', '192.168.0.256/32']
    monkeypatch.setattr('sys.argv', test_args)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.type == SystemExit
    assert exit_status.value.code == 1
