import sys

from unittest.mock import patch

import pytest

from systematic_networks.bin.netlookup import main


@patch.object(sys.stderr, 'write')
def test_commands_subtract_no_args(mock_method):
    """
    Test initializing subtract command
    """
    test_args = ['netlookup', 'subtract']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exit_code:
            main()
        assert exit_code.type == SystemExit
        assert exit_code.value.code == 2
    assert mock_method.called


@patch.object(sys.stderr, 'write')
def test_commands_subtract_substracted_no_subnets(mock_method):
    """
    Test initializing subtract command
    """
    test_args = ['netlookup', 'subtract', '-n', '192.168.0.0/33']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exit_code:
            main()
        assert exit_code.type == SystemExit
        assert exit_code.value.code == 1
    assert mock_method.called


@patch.object(sys.stderr, 'write')
def test_commands_subtract_invalid_subnets(mock_method):
    """
    Test initializing subtract command
    """
    test_args = [
        'netlookup', 'subtract',
        '-n', '192.168.0.0/29',
        '192.168.0.0/33'
    ]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exit_code:
            main()
        assert exit_code.type == SystemExit
        assert exit_code.value.code == 1
    assert mock_method.called


@patch.object(sys.stderr, 'write')
def test_commands_subtract_invalid_substracted_subnets(mock_method):
    """
    Test initializing subtract command
    """
    test_args = [
        'netlookup', 'subtract',
        '-n', '192.168.0.0/33',
        '192.168.0.0/24'
    ]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exit_code:
            main()
        assert exit_code.type == SystemExit
        assert exit_code.value.code == 1
    assert mock_method.called


@patch.object(sys.stdout, 'write')
def test_commands_subtract_valid_substracted_subnets(mock_method):
    """
    Test initializing subtract command
    """
    test_args = [
        'netlookup', 'subtract',
        '-n', '192.168.0.0/29,192.168.1.0/29',
        '192.168.0.0/24', '10.0.0.0/8'
    ]
    with patch.object(sys, 'argv', test_args):
        main()
    assert mock_method.called
