import sys

from unittest.mock import patch

import pytest

from systematic_networks.bin.netlookup import main
from systematic_networks.network import NetworkError


def mock_fail_vendor_update():
    """
    Method to mock error updating vendor data
    """
    raise NetworkError('Mock failed update')


@patch.object(sys.stderr, 'write')
def test_commands_prefixes_no_args(mock_method):
    """
    Test initializing prefixes command
    """
    test_args = ['netlookup', 'prefixes']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exit_code:
            main()
        assert exit_code.type == SystemExit
        assert exit_code.value.code == 1
    assert mock_method.called


def test_commands_prefixes_update_cache():
    """
    Test updating prefixes cache
    """
    test_args = ['netlookup', 'prefixes', '--update']
    with patch.object(sys, 'argv', test_args):
        main()


@patch.object(sys.stderr, 'write')
def test_commands_prefixes_update_cache_fail(mock_method):
    """
    Test updating prefixes cache
    """
    test_args = ['netlookup', 'prefixes', '--update']
    with patch('systematic_networks.prefixes.AWS.fetch', mock_fail_vendor_update):
        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit) as exit_code:
                main()
            assert exit_code.type == SystemExit
            assert exit_code.value.code == 1
    assert mock_method.called


@patch.object(sys.stdout, 'write')
def test_commands_prefixes_lookup_known_address(mock_method):
    """
    Test lookup for address in prefixes cache
    """
    test_args = ['netlookup', 'prefixes', '8.34.223.255']
    with patch.object(sys, 'argv', test_args):
        main()
    assert mock_method.called


@patch.object(sys.stdout, 'write')
def test_commands_prefixes_lookup_internal_address(mock_method):
    """
    Test lookup for address not in prefixes cache
    """
    test_args = ['netlookup', 'prefixes', '192.168.0.1']
    with patch.object(sys, 'argv', test_args):
        main()
    assert not mock_method.called


@patch.object(sys.stderr, 'write')
def test_commands_prefixes_lookup_invalid_address(mock_method):
    """
    Test lookup for invalid address
    """
    test_args = ['netlookup', 'prefixes', 'foobar']
    with patch.object(sys, 'argv', test_args):
        main()
    assert mock_method.called
