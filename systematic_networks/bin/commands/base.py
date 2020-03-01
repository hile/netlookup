
from systematic_cli.command import Command

from ...network import Network


class BaseCommand(Command):
    """
    Netlookup base command
    """
    networks = []

    def parse_args(self, args):
        self.networks = []
        if 'subnets' in args:
            try:
                for arg in args.subnets:
                    self.networks.append(Network(arg))
            except Exception as error:
                self.exit(1, 'Error parsing subnets: {}'.format(error))

        return args
