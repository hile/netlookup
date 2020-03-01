
from .base import BaseCommand


class Info(BaseCommand):
    """
    Command for function for 'netlookup info' CLI command
    """

    name = 'info'
    help = 'Show subnet info'

    def print_network_details(self, network):
        """
        Show details for specified network
        """
        first = network.first_host
        last = network.last_host
        self.message('         CIDR {}'.format(network.cidr))
        self.message('      Netmask {}'.format(network.netmask))
        self.message('      Network {}'.format(network.network))
        if network.broadcast is not None:
            self.message('    Broadcast {}'.format(network.broadcast))
        if first is not None:
            self.message('   First host {}'.format(network.first_host))
        if last is not None:
            self.message('    Last host {}'.format(network.last_host))
        self.message('  Total hosts {}'.format(network.total_hosts))
        self.message('         Next {}'.format(network.next())) # noqa B305
        self.message('     Previous {}'.format(network.previous()))
        self.message('         Bits {}'.format(network.network.bits()))
        self.message('  Reverse DNS {}'.format(network.network.reverse_dns))

    def register_parser_arguments(self, parser):
        parser.add_argument('subnets', nargs='*', help='Subnets to process')

    def run(self, args):  # pylint: disable=W0613
        if not args.subnets:
            self.exit(1, 'No subnets specified')

        for network in self.networks:
            self.print_network_details(network)
