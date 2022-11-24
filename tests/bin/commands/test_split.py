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
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)
