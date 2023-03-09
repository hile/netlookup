#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.bin.commands.substract module
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from netlookup.bin.netlookup import NetLookupScript

NETWORKS_ARG = '--networks=10.0.0.0/24'


def test_netlookup_subtract_add_no_arguments(monkeypatch):
    """
    Test running command 'netlookup subtract' with no arguments
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'subtract']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)


def test_netlookup_subtract_add_no_subnets(monkeypatch):
    """
    Test running command 'netlookup subtract' with no subnets in arguments
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'subtract', NETWORKS_ARG]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_netlookup_subtract_splittable_network(capsys, monkeypatch, mock_prefixes_data, splittable_network):
    """
    Test running 'netlookup subtract' command with valid address values and networks to subtract
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'subtract', NETWORKS_ARG, splittable_network]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) > 0


# pylint: disable=unused-argument
def test_netlookup_subtract_invalid_network(capsys, monkeypatch, mock_prefixes_data, invalid_network):
    """
    Test running 'netlookup subtract' command with invalid address values and networks to subtract
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'subtract', NETWORKS_ARG, invalid_network]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert len(captured.err.splitlines()) == 1
    assert captured.out == ''
