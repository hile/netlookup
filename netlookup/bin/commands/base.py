
from cli_toolkit.command import Command

from ...network import Network


class BaseCommand(Command):
    """
    Netlookup base command
    """
    networks = []

    def parse_args(self, args=None, namespace=None):
        """
        Parse common arguments for netlookup commands
        """
        self.networks = []
        if 'subnets' in args:
            try:
                for arg in args.subnets:
                    self.networks.append(Network(arg))
            except Exception as error:
                self.exit(1, f'Error parsing subnets: {error}')
        return args
