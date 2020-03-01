
from ...prefixes import Prefixes
from .base import BaseCommand


class PrefixLookup(BaseCommand):
    """
    Command for function for 'netlookup prefixes' CLI command
    """

    name = 'prefixes'
    short_description = 'Lookup prefixes'

    def register_parser_arguments(self, parser):
        parser.add_argument('-u', '--update', action='store_true', help='Update prefix cache')
        parser.add_argument('addresses', nargs='*', help='Prefixes to lookup')

    def run(self, args):
        prefixes = Prefixes()

        if not args.update and not args.addresses:
            self.exit(1, 'No prefixes specified')

        if args.update:
            self.message('Update prefix caches ...')
            try:
                prefixes.update()
            except Exception as error:
                self.exit(1, 'Error updating prefix caches: {}'.format(error))

        for address in args.addresses:
            try:
                address = prefixes.find(address)
                if address:
                    self.message(address)
            except Exception as error:
                self.error('Error looking up address {}: {}'.format(address, error))
