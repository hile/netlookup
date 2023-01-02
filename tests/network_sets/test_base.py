"""
Unit tests for netlookup.network_sets.base module
"""
import pytest

from netaddr.ip import IPNetwork
from netlookup.exceptions import NetworkError
from netlookup.network_sets.base import NetworkSet

TEST_NETWORKS = (
    IPNetwork('10.0.0.0/8'),
    IPNetwork('172.31.0.0/16'),
    IPNetwork('192.168.1.0/24'),
    IPNetwork('192.168.1.64/29'),
    IPNetwork('192.168.1.96/28'),
    IPNetwork('192.168.2.0/24'),
)
MERGED_NETWORKS = (
    IPNetwork('10.0.0.0/8'),
    IPNetwork('172.31.0.0/16'),
    IPNetwork('192.168.1.0/24'),
    IPNetwork('192.168.2.0/24'),
)
INVALID_NETWORK = '192.168.10.300/35'
NEW_NETWORK = IPNetwork('192.168.10.0/24')
KNOWN_ADDRESS = '192.168.1.65'
MISSING_ADDRESS = '4.3.2.1'


def test_network_sets_base_empty_properties():
    """
    Test properties of an empty NetworkSet
    """
    obj = NetworkSet()
    assert obj.cache_file is None

    assert len(obj) == 0
    # Plain, empty NetworkSet objects have no fetch() implementation
    with pytest.raises(NotImplementedError):
        obj.fetch()

    # This also attempts to trigger fetch() for empty network and fails
    with pytest.raises(NotImplementedError):
        next(obj)

    # Saving a base network set fails, there is no cache filename
    with pytest.raises(NetworkError):
        obj.save()


def test_network_sets_base_explicit_properties():
    """
    Test properties of a NetworkSet initialized with explicit networks
    """
    obj = NetworkSet(TEST_NETWORKS)
    assert obj.cache_file is None
    merged = obj.merged
    assert len(merged) == len(MERGED_NETWORKS)


def test_network_sets_base_add_network_existing():
    """
    Test adding existing network to a NetworkSet (will not change the network set)
    """
    obj = NetworkSet(TEST_NETWORKS)
    assert len(obj) == len(TEST_NETWORKS)
    obj.add_network(TEST_NETWORKS[0])
    assert len(obj) == len(TEST_NETWORKS)


def test_network_sets_base_add_network_new():
    """
    Test adding new network to a NetworkSet (will change the network set)
    """
    obj = NetworkSet(TEST_NETWORKS)
    assert len(obj) == len(TEST_NETWORKS)
    obj.add_network(NEW_NETWORK)
    assert len(obj) == len(TEST_NETWORKS) + 1


def test_network_sets_base_add_network_invalid_value():
    """
    Test adding new network to a NetworkSet (will change the network set)
    """
    obj = NetworkSet(TEST_NETWORKS)
    assert len(obj) == len(TEST_NETWORKS)
    with pytest.raises(NetworkError):
        obj.add_network(INVALID_NETWORK)


def test_network_sets_base_substract_network_existing():
    """
    Test subtracting existing network from a NetworkSet
    """
    obj = NetworkSet(TEST_NETWORKS)
    assert len(obj) == len(TEST_NETWORKS)
    removed = TEST_NETWORKS[:2]
    shorter = obj.substract(removed)
    # Contains the two last networks only from ipset
    assert len(shorter) == 2


def test_network_sets_base_substract_network_missing():
    """
    Test subtracting missing network from a NetworkSet
    """
    obj = NetworkSet(TEST_NETWORKS)
    assert len(obj) == len(TEST_NETWORKS)
    shorter = obj.substract('192.168.10.0/24')
    # Contains the minimized IP set instead of overlapping networks
    assert len(shorter) == len(MERGED_NETWORKS)


def test_network_sets_base_substract_network_invalid():
    """
    Test subtracting missing network from a NetworkSet
    """
    obj = NetworkSet(TEST_NETWORKS)
    assert len(obj) == len(TEST_NETWORKS)
    with pytest.raises(NetworkError):
        obj.substract(INVALID_NETWORK)


def test_network_sets_base_find_valid_address():
    """
    Test looking up a known address from base network set
    """
    assert isinstance(NetworkSet(TEST_NETWORKS).find(KNOWN_ADDRESS), IPNetwork)


def test_network_sets_base_find_missing_address():
    """
    Test looking up a known address from base network set
    """
    assert NetworkSet(TEST_NETWORKS).find(MISSING_ADDRESS) is None
