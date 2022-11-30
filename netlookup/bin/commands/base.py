
from cli_toolkit.command import Command

from ...network import Network


class BaseCommand(Command):
    """
    Netlookup base command
    """
    networks = []

    def __init__(self, parent, usage=None, description=None, epilog=None):
        super().__init__(parent, usage, description, epilog)
        self.errors = []

    def error(self, *args) -> None:
        """
        Add error to self.errors and send it to parent class method
        """
        self.errors.append(f'{self.__parse_string_args__(*args)}')
        super().error(*args)

    def parse_args(self, args=None, namespace=None):
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
