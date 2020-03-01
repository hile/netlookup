
import sys

from unittest.mock import patch

import pytest

from systematic_networks.bin.netlookup import main


def mock_message_callback(*args):
    """
    Test message callback is called
    """
    print(*args)


@patch.object(sys.stderr, 'write')
def test_commands_info_no_args(mock_method):
    """
    Test initializing Info command parse_args
    """
    test_args = ['netlookup', 'info']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exit_code:
            main()
        assert exit_code.type == SystemExit
        assert exit_code.value.code == 1
    assert mock_method.called


@patch.object(sys.stdout, 'write')
def test_commands_info_run_with_subnet(mock_method):
    """
    Test initializing info with subnets
    """
    test_args = ['netlookup', 'info', '192.168.0.0/24', '192.168.0.255/32']
    with patch.object(sys, 'argv', test_args):
        main()
    assert mock_method.called


@patch.object(sys.stderr, 'write')
def test_commands_info_run_invalid_subnets(mock_method):
    """
    Test initializing info with invalid subnets
    """
    test_args = ['netlookup', 'info', '192.168.0.256/32']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exit_code:
            main()
            assert exit_code.type == SystemExit
            assert exit_code.value.code == 1
    assert mock_method.called
