"""
Unit tests for netlookup.bin.commands.prefixes module
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from netlookup.bin.netlookup import NetLookupScript


def test_netlookup_prefixes_add_no_arguments(monkeypatch):
    """
    Test running command 'netlookup prefixes' with no arguments
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'prefixes']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)
