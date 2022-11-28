
from operator import attrgetter
from pathlib import Path

from .network import NetworkList, NetworkError, find_address_in_networks
from .network_sets.constants import DEFAULT_CACHE_DIRECTORY
from .network_sets.aws import AWS
from .network_sets.google import GoogleServices
from .network_sets.google_cloud import GoogleCloud


class Prefixes(NetworkList):
    """
    Loader and lookup for known IP address prefix caches for public clouds
    """
    def __init__(self, cache_directory=None) -> None:
        super().__init__()
        cache_directory = cache_directory if cache_directory is not None else DEFAULT_CACHE_DIRECTORY
        self.cache_directory = Path(cache_directory).expanduser()

        self.vendors = [
            AWS(cache_directory=self.cache_directory),
            GoogleCloud(cache_directory=self.cache_directory),
            GoogleServices(cache_directory=self.cache_directory),
        ]

        self.load()

    def update(self) -> None:
        """
        Fetch and update cached prefix data
        """
        for vendor in self.vendors:
            try:
                vendor.fetch()
                vendor.save()
            except Exception as error:
                raise NetworkError(f'Error updating {vendor} data: {error}') from error
        self.load()

    def save(self) -> None:
        """
        Save cached data for vendors
        """
        for vendor in self.vendors:
            vendor.save()

    def load(self) -> None:
        """
        Load cached networks
        """
        self.clear()
        for vendor in self.vendors:
            vendor.load()
            # Go directly to attribute, iterating vendor may trigger fetch
            for prefix in vendor.__networks__:
                self.append(prefix)
        self.sort(key=attrgetter('value'))

    def filter_type(self, value):
        """
        Filter networks by type
        """
        return [prefix for prefix in self if prefix.type == value]

    def get_vendor(self, name):
        """
        Get vendor prefix set
        """
        for vendor in self.vendors:
            if vendor.type == name:
                return vendor
        raise NetworkError(f'No such vendor: {name}')

    def find(self, value):
        """
        Find address in networks
        """
        return find_address_in_networks(self, value)
