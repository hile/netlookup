
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
        self.message(f'         CIDR {network.cidr}')
        self.message(f'      Netmask {network.netmask}')
        self.message(f'      Network {network.network}')
        if network.broadcast is not None:
            self.message(f'    Broadcast {network.broadcast}')
        if first is not None:
            self.message(f'   First host {network.first_host}')
        if last is not None:
            self.message(f'    Last host {network.last_host}')
        self.message(f'  Total hosts {network.total_hosts}')
        self.message(f'         Next {network.next()}')  # noqa
        self.message(f'     Previous {network.previous()}')
        self.message(f'         Bits {network.network.bits()}')
        self.message(f'  Reverse DNS {network.network.reverse_dns}')

    def register_parser_arguments(self, parser):
        parser.add_argument('subnets', nargs='*', help='Subnets to process')

    def run(self, args):  # pylint: disable=W0613
        if not args.subnets:
            self.exit(1, 'No subnets specified')

        for network in self.networks:
            self.print_network_details(network)
