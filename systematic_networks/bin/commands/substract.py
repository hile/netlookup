
from systematic_networks.network import NetworkError
from systematic_networks.network_sets.base import NetworkSet

from .base import BaseCommand


class Subtract(BaseCommand):
    """
    Command for function for 'netlookup substract' CLI command
    """

    name = 'subtract'
    short_description = 'Substract subnet from specified subnets'

    def register_parser_arguments(self, parser):
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

    def parse_args(self, args):
        """
        Parse subnet arguments
        """
        args.networks = [
            network
            for arg in args.networks
            for network in arg.split(',')
        ]
        return args

    def run(self, args):
        """
        Substract subnets
        """
        if not args.subnets:
            self.exit(1, 'No subnets specified')

        try:
            networks = NetworkSet(networks=args.subnets).substract(args.networks)
        except NetworkError as error:
            self.exit(1, error)

        for network in networks:
            self.message(network.cidr)
