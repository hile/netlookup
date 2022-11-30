"""
Unit tests for netlookup.bin.commands.base module
"""
from cli_toolkit.script import Script
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from netlookup.bin.commands.base import BaseCommand

from ...conftest import INVALID_NETWORKS, VALID_NETWORKS


class MiniBaseCommand(BaseCommand):
    """
    Minimal base command for unit tests
    """
    name = 'test'

    def register_parser_arguments(self, parser):
        """
        Register the 'subnets' argument to parser
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument('subnets', nargs='*', help='Subnets to process')
        return parser

    def run(self, args):
        """
        List networks parsed from the args
        """
        for network in self.networks:
            self.message(f'network {network}')


class BaseTestScript(Script):
    """
    Script to test the BaseCommand class
    """
    subcommands = (
        MiniBaseCommand,
    )


def test_commands_base_subnets_no_networks(monkeypatch, capsys):
    """
    Test parsing of the subnets list with no networks
    """
    script = BaseTestScript()
    testargs = ['netlookup', 'test']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''


def test_commands_base_subnets_valid_networks(monkeypatch, capsys):
    """
    Test parsing of the subnets list with valid networks
    """
    script = BaseTestScript()
    testargs = ['netlookup', 'test'] + list(VALID_NETWORKS)
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    assert len(lines) == len(VALID_NETWORKS)


def test_commands_base_subnets_invalid_networks(monkeypatch, capsys):
    """
    Test parsing of list of invalid networks as arguments
    """
    script = BaseTestScript()
    testargs = ['netlookup', 'test'] + list(INVALID_NETWORKS)
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1
