#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI utility to split a network from another
"""
from argparse import ArgumentParser, Namespace
from netlookup.network import NetworkError
from netlookup.network_sets.base import NetworkSet

from .base import BaseCommand


class Subtract(BaseCommand):
    """
    Command for function for 'netlookup substract' CLI command
    """
    name: str = 'subtract'
    short_description: str = 'Substract subnet from specified subnets'

    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Register arguments for subtracted networks
        """
        parser.add_argument(
            '-n', '--networks',
            action='append',
            required=True,
            help='Subnets to subtract'
        )
        parser.add_argument(
            'subnets',
            nargs='*',
            help='Subnets to subtract from'
        )
        return parser

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
        """
        Parse subnet arguments
        """
        args.networks = [
            network
            for arg in args.networks
            for network in arg.split(',')
        ]
        return args

    def run(self, args: Namespace) -> None:
        """
        Substract subnets and print the split ranges
        """
        if not args.subnets:
            self.exit(1, 'No subnets specified')

        try:
            networks = NetworkSet(networks=args.subnets).substract(args.networks)
        except NetworkError as error:
            self.exit(1, error)

        for network in networks:
            self.message(network.cidr)
