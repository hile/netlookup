"""
CLI command 'netlookup prefixes'
"""
from typing import List, Optional
from ...prefixes import Prefixes
from .base import BaseCommand


class PrefixLookup(BaseCommand):
    """
    Command for function for 'netlookup prefixes' CLI command
    """
    name = 'prefixes'
    short_description = 'Lookup prefixes'
    __prefixes__: Optional[Prefixes] = None

    def register_parser_arguments(self, parser):
        parser.add_argument('-u', '--update', action='store_true', help='Update prefix cache')
        parser.add_argument('addresses', nargs='*', help='Prefixes to lookup')

    @property
    def prefixes(self) -> Prefixes:
        """
        Return  a cached Prefixes object
        """
        if self.__prefixes__ is None:
            self.__prefixes__ = Prefixes()
        return self.__prefixes__

    def update_prefix_cache(self) -> None:
        """
        Update the prefix cache
        """
        self.message('Update prefix caches')
        try:
            self.prefixes.update()
        except Exception as error:
            self.exit(1, f'Error updating prefix caches: {error}')

    def lookup_addresses(self, addresses: List[str]) -> None:
        """
        Look up and print prefix addresses
        """
        for address in addresses:
            try:
                address = self.prefixes.find(address)
                if address:
                    self.message(address)
            except Exception as error:
                self.error(f'Error looking up address "{address}": {error}')

    def run(self, args):
        """
        Run 'netlookup prefixes' command
        """
        if not args.update and not args.addresses:
            self.exit(1, 'No prefixes specified')
        if args.update:
            self.update_prefix_cache()
        if args.addresses:
            self.lookup_addresses(args.addresses)
        if self.errors:
            self.exit(1)
