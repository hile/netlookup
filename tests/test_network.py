"""
Unit tests for netlookup.network module
"""
import pytest

from netaddr.ip import IPAddress, AddrFormatError

from netlookup.network import Network, NetworkError, parse_address_or_network

from .utils import validate_network, validate_network_compare_methods


def test_networks_parse_address_or_network_valid_values(mock_valid_network) -> None:
    """
    Unit tests for the parse_address_or_network function with valid
    values
    """
    value = parse_address_or_network(mock_valid_network)
    isinstance(value, IPAddress)


def test_networks_parse_address_or_network_invalid_values(mock_invalid_network) -> None:
    """
    Unit tests for the parse_address_or_network function with valid
    values
    """
    with pytest.raises(NetworkError):
        parse_address_or_network(mock_invalid_network)


def test_networks_network_valid_objects(mock_valid_network):
    """
    Test loading of valid network strings as Network objects
    """
    network = Network(mock_valid_network)
    validate_network(network)
    validate_network_compare_methods(network)


def test_networks_network_invalid_objects(mock_invalid_network):
    """
    Test loading of invalid network strings as Network objects

    Depending on the invalid string either ValueError or AddrFormatError
    is raised by the parent class
    """
    with pytest.raises((ValueError, AddrFormatError)):
        Network(mock_invalid_network)


def test_network_first_host_values(mock_network_first_host_tuple):
    """
    Test various cases network first host in networks
    """
    network = mock_network_first_host_tuple[0]
    first_host_value = mock_network_first_host_tuple[1]
    assert Network(network).first_host == first_host_value


def test_network_last_host_values(mock_network_last_host_tuple):
    """
    Test various cases network last host in networks
    """
    network = mock_network_last_host_tuple[0]
    first_host_value = mock_network_last_host_tuple[1]
    assert Network(network).last_host == first_host_value
