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
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)
