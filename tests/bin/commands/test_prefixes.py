"""
Unit tests for netlookup.bin.commands.prefixes module
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from netlookup.bin.netlookup import NetLookupScript

from ...constants import PREFIXES_GOOGLE_CLOUD_MATCH, PREFIXES_NO_MATCH, INVALID_NETWORKS


def test_netlookup_prefixes_add_no_arguments(monkeypatch):
    """
    Test running command 'netlookup prefixes' with no arguments
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'prefixes']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_netlookup_prefixes_update(capsys, monkeypatch, mock_prefixes_data):
    """
    Test running 'netlookup prefixes --update' command
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'prefixes', '--update']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    assert len(lines) == 1


# pylint: disable=unused-argument
def test_netlookup_prefixes_update_error(
        capsys,
        monkeypatch,
        mock_prefixes_data,
        mock_google_dns_requests_error):
    """
    Test running 'netlookup prefixes --update' command with errors
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'prefixes', '--update']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    errors = captured.err.splitlines()
    assert len(errors) == 1
    lines = captured.out.splitlines()
    assert len(lines) == 1


# pylint: disable=unused-argument
def test_netlookup_prefixes_update_and_lookup(capsys, monkeypatch, mock_prefixes_data):
    """
    Test running 'netlookup prefixes --update ' command with MOCK_WHOIS_QUERY_ADDRESS
    as address lookup argument
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'prefixes', '--update', PREFIXES_GOOGLE_CLOUD_MATCH]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    # One line for the update message, one for address item
    assert len(lines) == 2


# pylint: disable=unused-argument
def test_netlookup_prefixes_lookup_no_match(capsys, monkeypatch, mock_prefixes_data):
    """
    Test running 'netlookup prefixes' command with an address that does not match prefixes
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'prefixes', PREFIXES_NO_MATCH]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''


# pylint: disable=unused-argument
def test_netlookup_prefixes_lookup_invalid_network(capsys, monkeypatch, mock_prefixes_data):
    """
    Test running 'netlookup prefixes ' command with invalid network value as address lookup argument
    """
    script = NetLookupScript()
    testargs = ['netlookup', 'prefixes', INVALID_NETWORKS[-1]]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert len(captured.err.splitlines()) == 1
    assert captured.out == ''
