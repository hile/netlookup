
import json
import tempfile

from pathlib import Path

import pytest

from netlookup.network_sets import base

from netlookup.network import NetworkError
from netlookup.prefixes import Prefixes
from netlookup.network_sets.aws import AWS, AWSPrefix
from netlookup.network_sets.azure import Azure, AzurePrefix
from netlookup.network_sets.gcp import GCP, GCPPrefix
from netlookup.network_sets.google import GoogleServices, GoogleServicePrefix

from ..constants import MATCH_PREFIXES_LOOKUPS, INVALID_ADDRESS_LOOKUPS

DATA_PATH = Path(__file__).parent.absolute().joinpath('data')

TEST_DATA_PREFIX_LEN = 4085
TEST_NETWORK_ADDRESSES = (
    {
        'address': '8.34.208.0',
        'network': '8.34.208.0/20',
    },
    {
        'address': '8.34.223.10',
        'network': '8.34.208.0/20',
    },
    {
        'address': '8.34.223.254',
        'network': '8.34.208.0/20',
    },
    {
        'address': '8.34.223.255',
        'network': '8.34.208.0/20',
    },
    {
        'address': '8.34.224.0',
    },
    {
        'address': '2c0f:fb50:4000::0',
        'network': '2c0f:fb50:4000::/36'
    },
    {
        'address': '2c0f:fb50:4000::10',
        'network': '2c0f:fb50:4000::/36'
    },
    {
        'address': '2c0f:fb50:4fff:ffff:ffff:ffff:ffff:fffe',
        'network': '2c0f:fb50:4000::/36'
    },
    {
        'address': '2c0f:fb50:4fff:ffff:ffff:ffff:ffff:ffff',
        'network': '2c0f:fb50:4000::/36'
    },
    {
        'address': '2c0f:fb50:5000::0'
    }
)
TEST_JSON_REQUIRED_FIELDS = ('type', 'cidr')
TEST_FILTER_COUNTS = {
    'invalidvalue': 0,
    'aws': 1414,
    'azure': 2574,
    'gcp': 72,
    'google': 25,
}


@pytest.fixture
def mock_open_permission_denied(monkeypatch):
    """
    Fixture to mock
    """
    # pylint: disable=unused-argument
    def permission_denied(*args):
        """
        Always return false for os.access
        """
        raise PermissionError
    monkeypatch.setattr(base.Path, 'open', permission_denied)


def validate_prefix_list(network_set, loader_class):
    """
    Validate prefix list
    """
    for network in network_set:
        assert isinstance(network, loader_class)

    for network in network_set:
        assert isinstance(network, loader_class)
        value = network.__repr__()
        assert isinstance(value, str)
        assert value == str(network)


def test_cloud_vendor_prefixes_networks_no_data():
    """
    Test creating networks with no data using new temporary directory
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    assert len(prefixes) == 0


def test_cloud_vendor_prefixes_missing_directory():
    """
    Test creating cache directory
    """
    tempdir = tempfile.mkdtemp()
    cache_directory = Path(tempdir, 'test')
    assert not cache_directory.exists()
    prefixes = Prefixes(cache_directory=cache_directory)
    assert cache_directory.exists()
    assert len(prefixes) == 0


# pylint: disable=unused-argument,redefined-outer-name
def test_cloud_vendor_prefixes_missing_directory_create_error(mock_path_mkdir_permission_denied):
    """
    Test creating cache directory
    """
    cache_directory = Path('/D78B28E2-14AC-47B7-90DF-DC2694651038')
    assert not cache_directory.exists()
    with pytest.raises(NetworkError):
        Prefixes(cache_directory=cache_directory)
    assert not cache_directory.exists()


def test_cloud_vendor_prefixes_networks_iterator_load():
    """
    Test loading networks as side effect of iterator
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    for vendor in prefixes.vendors:
        assert len(vendor) == 0
        next(vendor)
        assert len(vendor) > 0


def test_cloud_vendor_prefixes_networks_save():
    """
    Test saving networks as side effect of iterator
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    for vendor in prefixes.vendors:
        assert len(vendor) == 0
        next(vendor)
        assert len(vendor) > 0
    prefixes.save()

    prefixes = Prefixes(cache_directory=tempdir)
    for vendor in prefixes.vendors:
        assert len(vendor) > 0


# pylint: disable=unused-argument
def test_cloud_vendor_prefixes_networks_save_no_permission(mock_open_permission_denied):
    """
    Test saving networks to files without permissions
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)

    for vendor in prefixes.vendors:
        assert len(vendor) == 0
        next(vendor)
        assert len(vendor) > 0

    with pytest.raises(NetworkError):
        prefixes.save()


def test_cloud_vendor_networks_loading():
    """
    Test creating networks with test data, ensuring correct number of networks is loaded
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    assert len(prefixes) == TEST_DATA_PREFIX_LEN


def test_cloud_vendor_prefix_filtering():
    """
    Test filtering cloud vendor prefixes
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    for name, count in TEST_FILTER_COUNTS.items():
        matches = prefixes.filter_type(name)
        assert len(matches) == count


def test_cloud_vendor_prefix_find_valid_addresses():
    """
    Test finding of addresses from cloud vendor prefixes
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    for value in MATCH_PREFIXES_LOOKUPS:
        address = prefixes.find(value)
        assert address is not None


def test_cloud_vendor_prefix_find_invalid_addresses():
    """
    Test finding of invalid address values from cloud vendor prefixes
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)

    for value in INVALID_ADDRESS_LOOKUPS:
        with pytest.raises(NetworkError):
            prefixes.find(value)


def test_cloud_vendor_prefix_lookup():
    """
    Test looking up networks from test data
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    for testcase in TEST_NETWORK_ADDRESSES:
        prefix = prefixes.find(testcase['address'])
        network = testcase.get('network', None)
        if network is not None:
            assert prefix is not None
            assert str(prefix.cidr) == network
        else:
            assert prefix is None


def test_cloud_vendor_json_formatting():
    """
    Test all loaded networks can be formatted as JSON
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    for prefix in prefixes:
        testdata = json.loads(json.dumps(prefix.as_dict()))
        for field in TEST_JSON_REQUIRED_FIELDS:
            assert field in testdata
            assert testdata[field] is not None


def test_cloud_vendor_prefixes_invalid_vendor():
    """
    Test cases for AWS prefixes
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    with pytest.raises(NetworkError):
        prefixes.get_vendor('8522A483-A895-40F3-B5BE-93DDDCA58E51')


def test_cloud_vendor_prefixes_aws():
    """
    Test cases for AWS prefixes
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    vendor = prefixes.get_vendor('aws')
    assert isinstance(vendor, AWS)
    validate_prefix_list(vendor, AWSPrefix)

    regions = vendor.regions
    assert isinstance(regions, list)
    for region in regions:
        assert isinstance(region, str)


def test_cloud_vendor_prefixes_azure():
    """
    Test cases for Azure prefixes
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    vendor = prefixes.get_vendor('azure')
    assert isinstance(vendor, Azure)
    validate_prefix_list(vendor, AzurePrefix)


def test_cloud_vendor_prefixes_gcp():
    """
    Test cases for GCP prefixes
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    vendor = prefixes.get_vendor('gcp')
    assert isinstance(vendor, GCP)
    validate_prefix_list(vendor, GCPPrefix)


def test_cloud_vendor_prefixes_google_services():
    """
    Test cases for google services prefixes
    """
    prefixes = Prefixes(cache_directory=DATA_PATH)
    vendor = prefixes.get_vendor('google')
    assert isinstance(vendor, GoogleServices)
    validate_prefix_list(vendor, GoogleServicePrefix)
