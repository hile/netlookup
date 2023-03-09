#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Base class for network set class
"""
import json

from datetime import datetime
from pathlib import Path
from typing import Optional

from netaddr.core import AddrFormatError
from netaddr.ip.sets import IPSet

from ..network import Network, NetworkList, NetworkError, find_address_in_networks


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

    def __repr__(self) -> str:
        return f'{self.type} {self.cidr}'

    def __str__(self) -> str:
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

    def __init__(self, networks=None, cache_directory=None) -> None:
        self.cache_directory = cache_directory
        self.updated = None
        self.__networks__ = NetworkList()
        self.__iter_index__ = None

        self.load()
        if networks is not None:
            for network in networks:
                self.add_network(network)

    def __len__(self) -> int:
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
        except IndexError as error:
            self.__iter_index__ = None
            raise StopIteration from error

    @property
    def cache_file(self) -> Optional[Path]:
        """
        Filename for prefix data cache file
        """
        if self.cache_filename is not None:
            return Path(self.cache_directory, self.cache_filename)
        return None

    @property
    def ipset(self) -> IPSet:
        """
        IPSet of networks in network set
        """
        return IPSet([item.cidr for item in self.__networks__])

    @property
    def merged(self):
        """
        Minimal merged set of IP range set covering network set
        """
        return self.__class__(networks=[self.loader_class(network) for network in self.ipset.iter_cidrs()])

    def fetch(self):
        """
        Fetch information for network
        """
        raise NotImplementedError('fetch() must be implemented in child class')

    def as_dict(self) -> dict:
        """
        Return all networks as dictionary
        """
        return {
            'updated': self.updated.isoformat() if self.updated else None,
            'networks': [prefix.as_dict() for prefix in self.__networks__]
        }

    def add_network(self, value) -> None:
        """
        Add network to cache
        """
        try:
            network = self.loader_class(value)
        except Exception as error:
            raise NetworkError(f'Error parsing network {value}: {error}') from error
        if network not in self.__networks__:
            self.__networks__.append(network)

    def substract(self, networks) -> None:
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
                raise NetworkError(f'Error processing network {network}: {error}') from error
        return self.__class__(networks=[self.loader_class(network) for network in ipset.iter_cidrs()])

    def __read_cache_file__(self):
        """
        Read network set data cache file
        """
        try:
            with self.cache_file.open('r', encoding='utf-8') as filedescriptor:
                return filedescriptor.read()
        except Exception as error:
            raise NetworkError(f'Error reading cache file {self.cache_file}: {error}') from error

    def load(self) -> None:
        """
        Load local cache file
        """
        if self.cache_file is None or not self.cache_file.is_file():
            return

        data = self.__read_cache_file__()
        try:
            data = json.loads(data)
        except Exception as error:
            raise NetworkError(f'Error parsing JSON data from cache file {self.cache_file}: {error}') from error

        self.__networks__.clear()
        try:
            self.updated = datetime.fromisoformat(data['updated'])
            for record in data['networks']:
                prefix = self.loader_class(record['cidr'], record)
                self.__networks__.append(prefix)
        except Exception as error:
            raise NetworkError(f'Error loading data from cache file {self.cache_file}: {error}') from error

    def save(self) -> None:
        """
        Save data to cache file
        """
        if self.cache_file is None:
            raise NetworkError(f'Network set does not define cache filename: {self}')
        try:
            with self.cache_file.open('w', encoding='utf-8') as filedescriptor:
                filedescriptor.write(f'{json.dumps(self.as_dict(), indent=2)}\n')
        except Exception as error:
            raise NetworkError(f'Error writing cache file {self.cache_file}: {error}') from error

    def find(self, value):
        """
        Find address in networks
        """
        return find_address_in_networks(self.__networks__, value)
