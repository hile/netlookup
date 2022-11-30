
from .base import BaseCommand


class Split(BaseCommand):
    """
    Command for function for 'netlookup split' CLI command
    """

    name = 'split'
    short_description = 'Show split subnet to prefixes'

    def register_parser_arguments(self, parser):
        parser.add_argument(
            '-m', '--mask',
            type=int,
            help='Mask for split networks'
        )
        parser.add_argument(
            'subnets',
            nargs='*',
            help='Subnets to process'
        )

    def run(self, args):
        if not args.subnets:
            self.exit(1, 'No subnets specified')

        for network in self.networks:
            prefixlen = args.mask if args.mask is not None else network.next_subnet_prefix
            if prefixlen is not None:
                for subnet in network.subnet(prefixlen):
                    self.message(subnet)
            else:
                self.error(f'Network is not splittable {network}')
            if self.errors:
                self.exit(1)
