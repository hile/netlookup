
from pathlib import Path

import pytest

from netlookup.network import Network, NetworkError
from netlookup.network_sets.base import (
    NetworkSet,
    NetworkSetItem,
)

from ..constants import (
    VALID_SUBNET_VALUES,
    INVALID_SUBNET_VALUES,
    MAX_SPLITS,
    VALID_ADDRESS_LOOKUPS,
    INVALID_ADDRESS_LOOKUPS
)


INVALID_JSON_CACHE_FILE = Path(
    Path(__file__).absolute().parent,
    'data/invalid_json_data.json'
)

INVALID_NETWORK_SET_CACHE_FILE = Path(
    Path(__file__).absolute().parent,
    'data/invalid_network_set.json'
)


SUBSTRACT_CACHE_FILE = Path(
    Path(__file__).absolute().parent,
    'data/substract_networks.json'
)


class SubstractedNetworkSet(NetworkSet):
    """
    Dummy network set to test substracting
    """
    cache_filename = SUBSTRACT_CACHE_FILE.name

    def fetch(self):
        return


class InvalidDataNetworkSet(NetworkSet):
    """
    Dummy network set to load invalid data
    """
    cache_filename = INVALID_JSON_CACHE_FILE.name

    def fetch(self):
        return


class InvalidNetworkSet(NetworkSet):
    """
    Dummy network set to load invalid data
    """
    cache_filename = INVALID_NETWORK_SET_CACHE_FILE.name

    def fetch(self):
        return


def test_network_set_create_empty():
    """
    Create empty network set with various arguments
    """
    network_set = NetworkSet()
    assert isinstance(network_set, NetworkSet)


def test_network_set_add_valid_networks():
    """
    Test loading valid network prefixes to empty network set
    """
    network_set = NetworkSet()
    for network in VALID_SUBNET_VALUES:
        network_set.add_network(network)
    assert len(network_set) == len(VALID_SUBNET_VALUES)


def test_network_set_load_excplicit_valid_networks():
    """
    Test loading valid network prefixes as argument to network set
    """
    network_set = NetworkSet(networks=VALID_SUBNET_VALUES)
    assert len(network_set) == len(VALID_SUBNET_VALUES)
    for network in VALID_SUBNET_VALUES:
        network_set.add_network(network)
    assert len(network_set) == len(VALID_SUBNET_VALUES)


def test_network_set_load_invalid_networks_data():
    """
    Test loading invalid data file
    """
    with pytest.raises(NetworkError):
        InvalidNetworkSet(
            cache_directory=INVALID_NETWORK_SET_CACHE_FILE.parent
        )


def test_network_set_load_invalid_json_data():
    """
    Test loading invalid JSON data file
    """
    with pytest.raises(NetworkError):
        InvalidDataNetworkSet(
            cache_directory=INVALID_JSON_CACHE_FILE.parent
        )


def test_network_set_find_valid_addresses():
    """
    Test find for valid addresses from file
    """
    network_set = NetworkSet(networks=VALID_SUBNET_VALUES)
    for value in VALID_ADDRESS_LOOKUPS:
        address = network_set.find(value)
        assert address is not None, f'error looking up {value}'
        print(address)

    address = network_set.find('127.0.0.1')
    assert address is None
    address = network_set.find('::1')
    assert address is None


def test_network_set_find_invalid_addresses():
    """
    Test find for invalid addresses from file
    """
    network_set = NetworkSet(networks=VALID_SUBNET_VALUES)
    for value in INVALID_ADDRESS_LOOKUPS:
        with pytest.raises(NetworkError):
            network_set.find(value)


def test_network_set_substraction():
    """
    Test find for invalid addresses from file with two /24 networks
    making a joined /23
    """
    network_set = SubstractedNetworkSet(cache_directory=SUBSTRACT_CACHE_FILE.parent)
    substracted = network_set.substract(['192.168.2.0/24', '10.0.0.0/8'])
    assert isinstance(substracted, list)
    assert len(substracted) == 1
    for value in substracted:
        assert isinstance(value, NetworkSetItem)

    network = '192.168.1.64/29'
    expected = [
        '192.168.0.0/24',
        '192.168.1.0/26',
        '192.168.1.72/29',
        '192.168.1.80/28',
        '192.168.1.96/27',
        '192.168.1.128/25'
    ]
    substracted = network_set.substract(network)
    print(substracted)
    assert isinstance(substracted, list)
    assert len(substracted) == len(expected)
    for value in substracted:
        assert str(value.cidr) in expected


def test_network_set_load_no_permissions():
    """
    Test loading network set with data file having no permissions
    """
    INVALID_NETWORK_SET_CACHE_FILE.chmod(int('0000', 8))
    with pytest.raises(NetworkError):
        InvalidNetworkSet(
            cache_directory=INVALID_NETWORK_SET_CACHE_FILE.parent
        )
    INVALID_NETWORK_SET_CACHE_FILE.chmod(int('0644', 8))


def test_network_set_save_no_filename():
    """
    Test saving network set with no cache filename set
    """
    network_set = NetworkSet()
    with pytest.raises(NetworkError):
        network_set.save()


def test_network_set_add_invalid_networks():
    """
    Test loading invalid network prefixes to empty network set
    """
    network_set = NetworkSet()
    for network in INVALID_SUBNET_VALUES:
        with pytest.raises(NetworkError):
            network_set.add_network(network)
    network_count = len(network_set)
    assert network_count == 0


def test_network_set_merged_empty():
    """
    Teste 'merged' property for empty network set
    """
    network_set = NetworkSet()
    assert network_set.merged == []


def test_network_set_merge_valid_networks():
    """
    Test merging valid network ranges
    """
    network_set = NetworkSet()
    expected = 0
    for network in VALID_SUBNET_VALUES:
        # Ignore global masks
        if Network(network).prefixlen == 0:
            continue
        network_set.add_network(network)
        expected += 1
    merged = network_set.merged
    assert len(merged) == expected


def test_network_set_merge_split_ranges():
    """
    Test merging split IP ranges

    Splits the range to smaller units and ensures the network set still only contains
    the original split network
    """
    network_set = NetworkSet()
    network = Network('172.31.4.0/22')
    network_set.add_network(network)

    network_count = 1
    for i in range(1, MAX_SPLITS + 1):
        prefixlen = network.prefixlen + i
        for subnet in network.subnet(prefixlen):
            network_set.add_network(subnet)
            network_count += 1
            assert len(network_set) == network_count
            assert len(network_set.merged) == 1
