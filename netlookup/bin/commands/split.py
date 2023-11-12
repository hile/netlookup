#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI tool to split network prefixes
"""
from argparse import ArgumentParser, Namespace

from .base import BaseCommand


class Split(BaseCommand):
    """
    Command for function for 'netlookup split' CLI command
    """
    name: str = 'split'
    short_description: str = 'Show split subnet to prefixes'

    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Add CLI arguments for netmask and subnet list
        """
        parser.add_argument(
            '-a', '--address-only',
            action='store_true',
            help='Omit mask from output'
        )
        parser.add_argument(
            '-m', '--mask',
            type=int,
            help='Mask for split networks'
        )
        parser.add_argument(
            'subnets',
            nargs='*',
            help='Subnets to split'
        )
        return parser

    def run(self, args: Namespace) -> None:
        """
        Run command, splitting networks and printing results on stdout
        """
        if not args.subnets:
            self.exit(1, 'No subnets specified')

        for network in self.networks:
            prefixlen = args.mask if args.mask is not None else network.next_subnet_prefix
            if prefixlen is not None:
                for subnet in network.subnet(prefixlen):
                    if args.address_only:
                        self.message(subnet.ip)
                    else:
                        self.message(subnet)
            else:
                self.error(f'Network is not splittable {network}')
            if self.errors:
                self.exit(1)
