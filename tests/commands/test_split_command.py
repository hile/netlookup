import sys

from unittest.mock import patch

import pytest

from systematic_networks.bin.netlookup import main


@patch.object(sys.stderr, 'write')
def test_commands_split_no_args(mock_method):
    """
    Test initializing split command
    """
    test_args = ['netlookup', 'split']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exit_code:
            main()
        assert exit_code.type == SystemExit
        assert exit_code.value.code == 1
    assert mock_method.called


@patch.object(sys.stderr, 'write')
def test_commands_split_run_with_subnets_invalid_mask(mock_method):
    """
    Test initializing split with subnets
    """
    test_args = ['netlookup', 'split', '--mask', '23', '192.168.0.0/24']
    with patch.object(sys, 'argv', test_args):
        main()
    assert mock_method.called


@patch.object(sys.stderr, 'write')
def test_commands_split_run_with_subnets_unsplittable(mock_method):
    """
    Test initializing split with subnets
    """
    test_args = ['netlookup', 'split', '192.168.0.0/32']
    with patch.object(sys, 'argv', test_args):
        main()
    assert mock_method.called


@patch.object(sys.stdout, 'write')
def test_commands_split_run_with_subnets_default_split(mock_method):
    """
    Test initializing split with subnets
    """
    test_args = ['netlookup', 'split', '192.168.0.0/24']
    with patch.object(sys, 'argv', test_args):
        main()
    assert mock_method.called


@patch.object(sys.stdout, 'write')
def test_commands_split_run_with_subnets_explicit_mask(mock_method):
    """
    Test initializing split with subnets
    """
    test_args = ['netlookup', 'split', '--mask', '26', '192.168.0.0/24']
    with patch.object(sys, 'argv', test_args):
        main()
    assert mock_method.called
