"""
Unit tests for netlookup.network module
"""
import pytest

from netaddr.ip import IPAddress, AddrFormatError

from netlookup.constants import IPV4_VERSION, IPV6_VERSION, MAX_PREFIX_LEN_IPV4, MAX_PREFIX_LEN_IPV6
from netlookup.network import (
    Network,
    NetworkError,
    find_address_in_networks,
    parse_address_or_network
)

from .constants import MAX_SPLITS
from .utils import validate_network, validate_network_compare_methods


def test_networks_parse_address_or_network_valid_values(valid_network) -> None:
    """
    Unit tests for the parse_address_or_network function with valid
    values
    """
    value = parse_address_or_network(valid_network)
    isinstance(value, IPAddress)
    assert parse_address_or_network(value) == value


def test_networks_parse_address_or_network_invalid_values(invalid_network) -> None:
    """
    Unit tests for the parse_address_or_network function with valid
    values
    """
    with pytest.raises(NetworkError):
        parse_address_or_network(invalid_network)


def test_network_find_address_in_networks_match_not_found(valid_network_list):
    """
    Test looking up address from list of networks with match found
    """
    assert find_address_in_networks(valid_network_list, '192.168.62.12') is None


def test_network_find_address_in_networks_match_found(valid_network_list):
    """
    Test looking up address from list of networks with match found
    """
    assert isinstance(find_address_in_networks(valid_network_list, '192.168.64.0'), Network)
    assert isinstance(find_address_in_networks(valid_network_list, '192.168.64.12'), Network)


def test_network_split_valid_networks(valid_network):
    """
    Test splitting of valid network values
    """
    network = Network(valid_network)
    prefixlen = network.prefixlen + 1
    if prefixlen == 0:
        prefixlen += 1

    if network.version == IPV4_VERSION:
        max_prefixlen = MAX_PREFIX_LEN_IPV4
    elif network.version == IPV6_VERSION:
        max_prefixlen = MAX_PREFIX_LEN_IPV6
    else:
        raise ValueError(f'Unexpected network address {network}')

    while prefixlen < max_prefixlen and prefixlen < network.prefixlen + MAX_SPLITS:
        testdata = list(network.subnet(prefixlen))
        assert len(testdata) > 0
        prefixlen += 1


def test_network_compare_ipv4_networks():
    """
    Test comparing IPv4 networks
    """
    a = Network('1.2.3.0/29')
    b = Network('192.168.64.0/24')

    assert a == a  # pylint: disable=comparison-with-itself
    assert a < b
    assert b > a
    assert a <= b
    assert b >= a

    assert a <= a  # pylint: disable=comparison-with-itself
    assert b >= b  # pylint: disable=comparison-with-itself


def test_network_compare_ipv4_network_to_address():
    """
    Test comparing IPv4 network to IP address
    """
    a = Network('192.168.64.0/24')
    b = IPAddress('193.194.195.196')

    assert not a == b  # pylint: disable=unneeded-not
    assert not b < a  # pylint: disable=unneeded-not
    assert a < b
    assert b > a
    assert a <= b
    assert b >= a


def test_network_compare_ipv4_network_to_string():
    """
    Test comparing IPv4 network to IP address
    """
    a = Network('10.0.0.0/8')
    b = Network('192.168.64.0/24')
    assert a == a.value
    assert a <= a.value
    assert a >= a.value
    assert a < b.value
    assert b > a.value


def test_network_subnet_split_invalid_values():
    """
    Test various cases of errors in splitting network
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


def test_networks_network_valid_objects(valid_network):
    """
    Test loading of valid network strings as Network objects
    """
    network = Network(valid_network)
    validate_network(network)
    validate_network_compare_methods(network)


def test_networks_network_invalid_objects(invalid_network):
    """
    Test loading of invalid network strings as Network objects

    Depending on the invalid string either ValueError or AddrFormatError
    is raised by the parent class
    """
    with pytest.raises((ValueError, AddrFormatError)):
        Network(invalid_network)


def test_network_host_count(network_host_count_value):
    """
    Test network host count for subnets
    """
    network = network_host_count_value[0]
    total_hosts = network_host_count_value[1]
    assert Network(network).total_hosts == total_hosts


def test_network_first_host_values(network_first_host_tuple):
    """
    Test various cases network first host in networks
    """
    network = network_first_host_tuple[0]
    first_host_value = network_first_host_tuple[1]
    assert Network(network).first_host == first_host_value


def test_network_last_host_values(network_last_host_tuple):
    """
    Test various cases network last host in networks
    """
    network = network_last_host_tuple[0]
    first_host_value = network_last_host_tuple[1]
    assert Network(network).last_host == first_host_value
