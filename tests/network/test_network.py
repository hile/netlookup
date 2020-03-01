
import pytest

from netaddr.core import AddrFormatError
from netaddr.ip import IPAddress

from systematic_networks.network import Network, NetworkError, parse_address_or_network
from ..constants import VALID_SUBNET_VALUES, INVALID_SUBNET_VALUES


def validate_network_compare_methods(network):
    """
    Validate a network object's compare methods
    """
    host = network.first_host
    if host is not None:
        assert network != str(host)
        assert network != host
        assert network < str(host)
        assert network < host
        assert network <= str(host)
        assert network <= host
        assert str(host) > network
        assert host > network
        assert str(host) >= network
        assert host >= network

    try:
        next_network = network.next()
        assert next_network > network
        assert next_network >= network
    except IndexError:
        # Past network range max, this is ok
        pass


def validate_network(network):
    """
    Validate a network object
    """
    assert isinstance(network, Network)
    assert isinstance(network.__repr__(), str)


def test_parse_address_or_network_valid_values():
    """
    Test various values for parse_address_or_network
    """
    value = parse_address_or_network('127.0.0.1')
    assert isinstance(value, IPAddress)
    assert value == parse_address_or_network(value)
    value = parse_address_or_network('10.0.0.0/32')
    assert isinstance(value, Network)
    assert value == parse_address_or_network(value)
    value = parse_address_or_network('::1')
    assert isinstance(value, IPAddress)
    assert value == parse_address_or_network(value)
    value = parse_address_or_network('::1/128')
    assert isinstance(value, Network)
    assert value == parse_address_or_network(value)


def test_parse_address_or_network_invalid_values():
    """
    Test parsing unexpected values for address or network
    """
    values = (
        'example.com',
        'foobar'
    )
    for value in values:
        with pytest.raises(NetworkError):
            print('test value', value)
            parse_address_or_network(value)


def test_network_valid_values():
    """
    Test valid network values
    """
    for value in VALID_SUBNET_VALUES:
        network = Network(value)
        validate_network(network)
        validate_network_compare_methods(network)


def test_network_invalid_values():
    """
    Test invalid network values
    """
    for value in INVALID_SUBNET_VALUES:
        with pytest.raises(AddrFormatError):
            Network(value)


def test_network_first_host():
    """
    Test various cases network first host in networks
    """
    assert Network('192.168.64.65/31').first_host == IPAddress('192.168.64.64')
    assert Network('192.168.64.65/32').first_host is None
    assert Network('2001::1/127').first_host == IPAddress('2001::0')
    assert Network('2001::1/128').first_host is None


def test_network_last_host():
    """
    Test various cases network first host in networks
    """
    assert Network('192.168.64.65/32').last_host is None
    assert Network('2001::1/128').last_host is None

    value = IPAddress('192.168.64.65')
    assert Network('192.168.64.65/31').last_host == value
    value = IPAddress('2001::1')
    assert Network('2001::1/127').last_host == value

    value = IPAddress('192.169.255.254')
    assert Network('192.168.8.96/15').last_host == value
    value = IPAddress('2001:999:61:2660:ffff:ffff:ffff:fffe')
    assert Network('2001:999:61:2660:2950::/64').last_host == value


def test_network_total_hosts():
    """
    Test various cases of total hosts count in networks
    """
    assert Network('192.168.0.1/31').total_hosts == 2
    assert Network('192.168.0.1/32').total_hosts == 1
    assert Network('2001::1/127').total_hosts == 2
    assert Network('2001::1/128').total_hosts == 1

    ipv4_values = ('0.0.0.0/0', '192.168.0.0/24')
    for value in ipv4_values:
        network = Network(value)
        assert network.total_hosts == network.size - 2

    ipv6_values = ('fe::1:2/64', 'fe::/12')
    for value in ipv6_values:
        network = Network(value)
        assert network.total_hosts == network.size - 2


def test_network_next_subnet_prefix():
    """
    Test various cases of network's next subnet prefix values
    """
    assert Network('192.168.64.65/32').next_subnet_prefix is None
    assert Network('2001::1/128').next_subnet_prefix is None

    values = (
        '192.168.0.1/31',
        '192.168.0.0/28',
        '2001::1/127',
        'fe::1:2/64',
    )
    for value in values:
        network = Network(value)
        assert network.next_subnet_prefix == network.prefixlen + 1


def test_network_parent_subnet_prefix():
    """
    Test various cases of network's next parent prefix values
    """
    assert Network('0.0.0.0/0').parent_subnet_prefix is None
    assert Network('0::/0').parent_subnet_prefix is None

    values = (
        '192.168.64.65/32',
        '192.168.0.1/31',
        '192.168.0.0/28',
        '2001::1/128',
        '2001::1/127',
        'fe::1:2/64',
    )
    for value in values:
        network = Network(value)
        assert network.parent_subnet_prefix == network.prefixlen - 1


def test_network_subnet_split_invalid_values():
    """
    Test various cases of network's next parent prefix values
    """
    values = (
        '192.168.64.65/32',
        '2001::1/128',
    )
    for value in values:
        with pytest.raises(AddrFormatError):
            network = Network(value)
            assert network.subnet(network.prefixlen + 1)

    values = (
        '192.168.0.1/31',
        '192.168.0.0/28',
    )
    for value in values:
        with pytest.raises(AddrFormatError):
            network = Network(value)
            assert network.subnet(network.prefixlen - 1)
    for value in values:
        with pytest.raises(AddrFormatError):
            network = Network(value)
            assert network.subnet(33)

    values = (
        '2001::1/127',
        'fe::1:2/64',
    )
    for value in values:
        with pytest.raises(AddrFormatError):
            network = Network(value)
            assert network.subnet(network.prefixlen - 1)
    for value in values:
        with pytest.raises(AddrFormatError):
            network = Network(value)
            assert network.subnet(129)
