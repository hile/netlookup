
import pytest

from netaddr.core import AddrFormatError

from netlookup.network import Network
from ..constants import VALID_SUBNET_VALUES, INVALID_SUBNET_VALUES, MAX_SPLITS


def validate_network(value):
    """
    Validate a network value
    """
    network = Network(value)
    return network


def test_subnet_valid_values():
    """
    Test parsing of valid values for subnet object
    """
    for value in VALID_SUBNET_VALUES:
        validate_network(value)


def test_subnet_invalid_values():
    """
    Test parsing of invalid values for subnet object
    """
    for value in INVALID_SUBNET_VALUES:
        with pytest.raises(AddrFormatError):
            validate_network(value)


def test_subnet_integer_compare_functions():
    """
    Test integer compare functions for extended subnet objects
    """
    for value in VALID_SUBNET_VALUES:
        network = validate_network(value)
        assert network == network.value
        assert network != network.value - 1
        assert network < network.last + 1
        assert network <= network.last
        assert network > network.value - 1
        assert network >= network.value


def test_first_host_property():
    """
    Test custom last_host property
    """
    for value in VALID_SUBNET_VALUES:
        network = validate_network(value)
        if network.version == 4 and network.prefixlen == 32:
            assert network.first_host is None
        elif network.version == 4 and network.prefixlen == 31:
            assert network.first_host.value == network.first
        elif network.version == 6 and network.prefixlen == 127:
            assert network.first_host.value == network.first
        elif network.version == 6 and network.prefixlen == 128:
            assert network.first_host is None
        else:
            assert network.first_host.value == network.first + 1


def test_subnet_last_host_property():
    """
    Test custom last_host property
    """
    for value in VALID_SUBNET_VALUES:
        network = validate_network(value)
        if network.version == 4 and network.prefixlen == 31:
            assert network.last_host.value, network.last
        elif network.version == 4 and network.prefixlen == 32:
            assert network.last_host is None
        elif network.version == 6 and network.prefixlen == 127:
            assert network.last_host.value == network.last
        elif network.version == 6 and network.prefixlen == 128:
            assert network.last_host is None
        else:
            assert network.last_host.value == network.last - 1


def test_subnnet_splitting_v4():
    """
    Test splitting IPv4 subnet
    """
    for value in VALID_SUBNET_VALUES:
        network = validate_network(value)
        if network.version == 4:
            prefixlen = network.prefixlen + 1
            if prefixlen == 0:
                prefixlen += 1
            while prefixlen < 32 and prefixlen < network.prefixlen + MAX_SPLITS:
                testdata = list(network.subnet(prefixlen))
                assert len(testdata) > 0
                prefixlen += 1


def test_splitting_v6_subnets():
    """
    Test splitting IPv4 subnets
    """
    for value in VALID_SUBNET_VALUES:
        network = validate_network(value)
        if network.version == 6:
            prefixlen = network.prefixlen + 1
            if prefixlen == 0:
                prefixlen += 1
            while prefixlen < 128 and prefixlen < network.prefixlen + MAX_SPLITS:
                testdata = list(network.subnet(prefixlen))
                assert len(testdata) > 0
                prefixlen += 1
