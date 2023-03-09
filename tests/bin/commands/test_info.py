#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.bin.commands.info module
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from netlookup.bin.netlookup import NetLookupScript


def test_netlookup_info_add_no_arguments(monkeypatch):
    """
    Test running command 'netlookup info' with no arguments
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'info']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_netlookup_prefixes_info_output(capsys, monkeypatch, mock_prefixes_data, valid_network):
    """
    Test running 'netlookup info' command with valid address valules
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'info', valid_network]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) > 0


# pylint: disable=unused-argument
def test_netlookup_prefixes_info_invalid_network(capsys, monkeypatch, mock_prefixes_data, invalid_network):
    """
    Test running 'netlookup info' command with valid address valules
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'info', invalid_network]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert len(captured.err.splitlines()) == 1
    assert captured.out == ''
