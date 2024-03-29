#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.bin.commands.split module
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from netlookup.bin.netlookup import NetLookupScript


def test_netlookup_split_add_no_arguments(monkeypatch):
    """
    Test running command 'netlookup split' with no arguments
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'split']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_netlookup_split_splittable_network(capsys, monkeypatch, mock_prefixes_data, splittable_network):
    """
    Test running 'netlookup split' command with valid and splittable address valules
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'split', splittable_network]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    assert len(lines) > 0
    for line in lines:
        assert line.count('/') == 1


# pylint: disable=unused-argument
def test_netlookup_split_splittable_network_address_only(capsys, monkeypatch, mock_prefixes_data, splittable_network):
    """
    Test running 'netlookup split' command with valid and splittable address valules
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'split', '--address-only', splittable_network]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    assert len(lines) > 0
    for line in lines:
        assert line.count('/') == 0


# pylint: disable=unused-argument
def test_netlookup_split_unsplittable_network(capsys, monkeypatch, mock_prefixes_data, unsplittable_network):
    """
    Test running 'netlookup split' command with valid but unsplittable address values
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'split', unsplittable_network]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert len(captured.err.splitlines()) == 1
    assert captured.out == ''


# pylint: disable=unused-argument
def test_netlookup_split_invalid_network(capsys, monkeypatch, mock_prefixes_data, invalid_network):
    """
    Test running 'netlookup split' command with valid address values
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'split', invalid_network]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert len(captured.err.splitlines()) == 1
    assert captured.out == ''
