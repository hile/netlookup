#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Extensions to netaddr objects as networks
"""
from bisect import bisect_left
from typing import Optional

from netaddr.ip import IPNetwork, IPAddress
from netaddr.core import AddrFormatError

from .constants import IPV4_VERSION, IPV6_VERSION, MAX_PREFIX_LEN_IPV4, MAX_PREFIX_LEN_IPV6
from .exceptions import NetworkError


def find_address_in_networks(networks, value):
    """
    Find given address in networks
    """
    address = parse_address_or_network(value)
    next_address = bisect_left(networks, address)
    if next_address > 0:
        try:
            prefix = networks[next_address]
            if address.value == prefix.value or address in prefix:
                return prefix
        except IndexError:
            pass
        prefix = networks[next_address - 1]
        if address.value == prefix.value or address in prefix:
            return prefix

    # Match to network address value (i.e. 192.168.1.0 for 192.168.1.0/24)
    for network in networks:
        if address.value == network.value:
            return network

    return None


def parse_address_or_network(value):
    """
    Parse value as IPAddress or Network
    """
    if isinstance(value, (IPAddress, Network)):
        return value
    try:
        return IPAddress(value)
    except (ValueError, AddrFormatError):
        pass
    try:
        return Network(value)
    except AddrFormatError as error:
        raise NetworkError(f'Error parsing address or network from {value}') from error


class NetworkList(list):
    """
    Base class for a list of networks
    """
    def clear(self):
        del self[:len(self)]


class Network(IPNetwork):
    """
    Extend IPNetwork with some custom attributes
    """
    def __eq__(self, other):
        if isinstance(other, str):
            other = parse_address_or_network(other)
        if isinstance(other, Network):
            return self.value == other.value and self.prefixlen == other.prefixlen
        if isinstance(other, IPAddress):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, str):
            return str(self.cidr) < other
        if isinstance(other, (Network, IPAddress)):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, str):
            return str(self.cidr) <= other
        if isinstance(other, (Network, IPAddress)):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, (Network, IPAddress)):
            return self.last > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, (Network, IPAddress)):
            return self.value >= other.value
        return self.value >= other

    @property
    def total_hosts(self):
        """
        Return total number of available hosts in subnet, excluding network and
        broadcast addresses
        """
        if self.version == IPV4_VERSION:
            if self.prefixlen == MAX_PREFIX_LEN_IPV4 - 1:
                return 2
            if self.prefixlen == MAX_PREFIX_LEN_IPV4:
                return 1
        if self.version == 6:
            if self.prefixlen == MAX_PREFIX_LEN_IPV6 - 1:
                return 2
            if self.prefixlen == MAX_PREFIX_LEN_IPV6:
                return 1
        return self.size - 2

    @property
    def first_host(self):
        """
        Return first available host in network, excluding network address
        """
        if self.version == IPV4_VERSION:
            if self.prefixlen == MAX_PREFIX_LEN_IPV4 - 1:
                return IPAddress(self.first)
            if self.prefixlen == MAX_PREFIX_LEN_IPV4:
                return None
        if self.version == IPV6_VERSION:
            if self.prefixlen == MAX_PREFIX_LEN_IPV6 - 1:
                return IPAddress(self.first)
            if self.prefixlen == MAX_PREFIX_LEN_IPV6:
                return None
        return IPAddress(self.first + 1)

    @property
    def last_host(self):
        """
        Return last available host in network, excluding broadcast address
        """
        if self.version == IPV4_VERSION:
            if self.prefixlen == MAX_PREFIX_LEN_IPV4 - 1:
                return IPAddress(self.last)
            if self.prefixlen == MAX_PREFIX_LEN_IPV4:
                return None
        if self.version == IPV6_VERSION:
            if self.prefixlen == MAX_PREFIX_LEN_IPV6 - 1:
                return IPAddress(self.last)
            if self.prefixlen == MAX_PREFIX_LEN_IPV6:
                return None
        return IPAddress(self.last - 1)

    @property
    def next_subnet_prefix(self) -> Optional[int]:
        """
        Return next subnet prefix size, i.e. smaller prefix than this

        May return None when item is already a host only network
        """
        if self.version == IPV4_VERSION:
            if self.prefixlen == MAX_PREFIX_LEN_IPV4:
                return None
        if self.version == IPV6_VERSION:
            if self.prefixlen == MAX_PREFIX_LEN_IPV6:
                return None
        return self.prefixlen + 1

    @property
    def parent_subnet_prefix(self) -> Optional[int]:
        """
        Return parent subnet prefix size, i.e. one larger prefix than this

        May return None when item is already 0
        """
        if self.prefixlen == 0:
            return None
        return self.prefixlen - 1

    @property
    def max_prefix_len(self) -> int:
        """
        Return largets allowed prefix length
        """
        return MAX_PREFIX_LEN_IPV4 if self.version == 4 else MAX_PREFIX_LEN_IPV6

    def subnet(self, prefixlen: int, count: Optional[int] = None, fmt: Optional[str] = None):
        """
        Return subnets split by specified prefix

        Adds extra validation for prefixlen, checking the value is not out off scope
        based on address type
        """
        prefixlen = int(prefixlen)
        if prefixlen < 0 or prefixlen > self.max_prefix_len:
            raise AddrFormatError(f'Invalid address prefixlen value: {prefixlen}')
        if prefixlen <= self.prefixlen:
            raise AddrFormatError(
                f'Split mask {prefixlen} is not valid for prefixlen {self.prefixlen}'
            )
        return super().subnet(prefixlen, count, fmt)
