#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common base command for netlookup CLI commands
"""
from argparse import Namespace
from typing import Any, List, Optional
from cli_toolkit.command import Command, NestedCliCommand

from ...network import Network


class BaseCommand(Command):
    """
    Netlookup base command
    """
    networks: List[Network] = []

    def __init__(self,
                 parent: NestedCliCommand,
                 usage: Optional[str] = None,
                 description: Optional[str] = None,
                 epilog: Optional[str] = None):
        super().__init__(parent, usage, description, epilog)
        self.errors = []

    def error(self, *args: List[Any]) -> None:
        """
        Add error to self.errors and send it to parent class method
        """
        self.errors.append(f'{self.__parse_string_args__(*args)}')
        super().error(*args)

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
        """
        Parse common arguments for netlookup commands
        """
        self.networks = []
        for subnet in getattr(args, 'subnets', []):
            try:
                self.networks.append(Network(subnet))
            except Exception as error:
                self.exit(1, f'Error parsing subnet "{subnet}": {error}')
        return args
