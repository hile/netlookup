
import json

from datetime import datetime
from pathlib import Path

from netaddr.core import AddrFormatError
from netaddr.ip.sets import IPSet

from ..network import Network, NetworkList, NetworkError, find_address_in_networks
from .configuration import get_cache_directory


class NetworkSetItem(Network):
    """
    Named network prefix for specific vendor and service
    """
    type = 'generic'
    extra_attributes = []

    def __init__(self, network, data=None):
        super().__init__(network)

        if data is not None:
            for attr in self.extra_attributes:
                if attr in data:
                    setattr(self, attr, data[attr])

    def __repr__(self):
        return '{} {}'.format(self.type, self.cidr)

    def __str__(self):
        return self.__repr__()

    def as_dict(self):
        """
        Format prefix object as dictionary

        Extend in child class to get prefix type specific data
        """
        data = {
            'type': self.type,
            'cidr': str(self.cidr)
        }
        for attr in self.extra_attributes:
            data[attr] = getattr(self, attr)
        return data


class NetworkSet:
    """
    Common base class for network address prefix sets with caching
    """
    type = 'generic'
    cache_filename = None
    loader_class = NetworkSetItem

    def __init__(self, cache_directory=None, networks=None):
        if cache_directory is None:
            cache_directory = get_cache_directory()
        self.cache_directory = Path(cache_directory).expanduser()
        self.updated = None
        self.__networks__ = NetworkList()
        self.__iter_index__ = None

        if not self.cache_directory.exists():
            try:
                self.cache_directory.mkdir(parents=True)
            except Exception as error:
                raise NetworkError('Error creating directory {}: {}'.format(self.cache_directory, error))

        self.load()
        if networks is not None:
            for network in networks:
                self.add_network(network)

    def __len__(self):
        return len(self.__networks__)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.__networks__:
            self.fetch()
        if self.__iter_index__ is None:
            self.__iter_index__ = 0
        try:
            item = self.__networks__[self.__iter_index__]
            self.__iter_index__ += 1
            return item
        except IndexError:
            self.__iter_index__ = None
            raise StopIteration

    @property
    def cache_file(self):
        """
        Filename for prefix data cache file
        """
        if self.cache_filename is not None:
            return Path(self.cache_directory, self.cache_filename)
        return None

    @property
    def ipset(self):
        """
        IPSet of networks in network set
        """
        return IPSet(self.__networks__)

    @property
    def merged(self):
        """
        Minimal merged set of IP range set covering network set
        """
        return [self.loader_class(network) for network in self.ipset.iter_cidrs()]

    def fetch(self):
        """
        Fetch information for network
        """
        raise NotImplementedError('fetch() must be implemented in child class')

    def as_dict(self):
        """
        Return all networks as dictionary
        """
        return {
            'updated': self.updated.isoformat() if self.updated else None,
            'networks': [prefix.as_dict() for prefix in self.__networks__]
        }

    def add_network(self, value):
        """
        Add network to cache
        """
        try:
            network = self.loader_class(value)
        except Exception as error:
            raise NetworkError('Error parsing network {}: {}'.format(value, error))
        if network not in self.__networks__:
            self.__networks__.append(network)

    def substract(self, networks):
        """
        Return merged network set, with specified network removed
        """
        ipset = self.ipset
        if isinstance(networks, str):
            networks = [networks]
        for network in networks:
            try:
                ipset.remove(network)
            except AddrFormatError as error:
                raise NetworkError('Error processing network {}: {}'.format(network, error))
        return [self.loader_class(network) for network in ipset.iter_cidrs()]

    def __read_cache_file__(self):
        """
        Read network set data cache file
        """
        try:
            with self.cache_file.open('r') as filedescriptor:
                return filedescriptor.read()
        except Exception as error:
            raise NetworkError('Error reading cache file {}: {}'.format(
                self.cache_file,
                error
            ))

    def load(self):
        """
        Load local cache file
        """
        if self.cache_file is None or not self.cache_file.is_file():
            return

        data = self.__read_cache_file__()
        try:
            data = json.loads(data)
        except Exception as error:
            raise NetworkError('Error parsing JSON data from cache file {}: {}'.format(
                self.cache_file,
                error
            ))

        self.__networks__.clear()
        try:
            self.updated = datetime.fromisoformat(data['updated'])
            for record in data['networks']:
                prefix = self.loader_class(record['cidr'], record)
                self.__networks__.append(prefix)
        except Exception as error:
            raise NetworkError('Error loading data from cache file {}: {}'.format(
                self.cache_file,
                error
            ))

    def save(self):
        """
        Save data to cache file
        """
        if self.cache_file is None:
            raise NetworkError(
                'Network set does not define cache filename: {}'.format(self)
            )
        try:
            with self.cache_file.open('w') as filedescriptor:
                filedescriptor.write('{}\n'.format(json.dumps(self.as_dict(), indent=2)))
        except Exception as error:
            raise NetworkError('Error writing cache file {}: {}'.format(
                self.cache_file,
                error
            ))

    def find(self, value):
        """
        Find address in networks
        """
        return find_address_in_networks(self.__networks__, value)
