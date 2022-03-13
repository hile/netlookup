"""
Unnit tests for netlookup.prefixes cloud address pool parsing
"""

import json
import tempfile

import pytest

from netlookup.network import NetworkError
from netlookup.prefixes import Prefixes

INVALID_URL = 'http://tuohela.net/invalid-url-test'

AZURE_DATA_EMPTY_REGION = {
    'test': [],
}
AZURE_DATA_STRING_REGION = {
    'test': '192.168.1.0/24',
}
AZURE_DATA_INVALID_REGION_PREFIX = {
    'test': ['example.com'],
}


def mock_invalid_json_data():
    """
    Mock invalid data string not in JSON format
    """
    return '{"invalid"}'


def mock_azure_empty_region_data():
    """
    Mock returning Azure data where region prefix list is empty
    """
    return json.dumps(AZURE_DATA_EMPTY_REGION)


def mock_azure_region_string_data():
    """
    Mock returning Azure data where region contains network prefix as string
    """
    return json.dumps(AZURE_DATA_STRING_REGION)


def mock_azure_region_invalid_prefix_data():
    """
    Mock returning Azure data where region contains invalid prefix
    """
    return json.dumps(AZURE_DATA_INVALID_REGION_PREFIX)


def test_cloud_vendor_networks_updating():
    """
    Test updating test data from network

    This test case requires internet connection
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    prefixes.update()
    assert len(prefixes) > 0

    for vendor in prefixes.vendors:
        assert len(vendor) > 0


def test_cloud_vendor_aws_fetch_error(monkeypatch):
    """
    Test failure fetching AWS data with HTTP
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    vendor = prefixes.get_vendor('aws')

    monkeypatch.setattr('netlookup.network_sets.aws.AWS_IP_RANGES_URL', INVALID_URL)
    with pytest.raises(NetworkError):
        vendor.fetch()


def test_cloud_vendor_aws_data_parse_error(monkeypatch):
    """
    Test failure updating AWS data
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    vendor = prefixes.get_vendor('aws')

    monkeypatch.setattr(vendor, '__get_aws_ip_ranges__', mock_invalid_json_data)
    with pytest.raises(NetworkError):
        vendor.fetch()


def test_cloud_vendor_azure_fetch_error(monkeypatch):
    """
    Test failure fetching Azure data with HTTP
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    vendor = prefixes.get_vendor('azure')

    monkeypatch.setattr('netlookup.network_sets.azure.AZURE_SERVICES_URL', INVALID_URL)
    with pytest.raises(NetworkError):
        vendor.fetch()


def test_cloud_vendor_azure_data_parse_error(monkeypatch):
    """
    Test failure updating Azure data
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    vendor = prefixes.get_vendor('azure')

    monkeypatch.setattr(vendor, '__get_azure_ip_ranges__', mock_invalid_json_data)
    with pytest.raises(NetworkError):
        vendor.fetch()


def test_cloud_vendor_azure_data_empty_region(monkeypatch):
    """
    Test updating Azure data with empty region item
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    vendor = prefixes.get_vendor('azure')

    monkeypatch.setattr(vendor, '__get_azure_ip_ranges__', mock_azure_empty_region_data)
    vendor.fetch()
    assert len(vendor) == 0


def test_cloud_vendor_azure_data_string_prefix_region(monkeypatch):
    """
    Test updating Azure data with string preffix region item
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    vendor = prefixes.get_vendor('azure')

    monkeypatch.setattr(vendor, '__get_azure_ip_ranges__', mock_azure_region_string_data)
    vendor.fetch()
    assert len(vendor) == 1


def test_cloud_vendor_azure_data_invalid_prefix_region(monkeypatch):
    """
    Test updating Azure data with string preffix region item
    """
    tempdir = tempfile.mkdtemp()
    prefixes = Prefixes(cache_directory=tempdir)
    vendor = prefixes.get_vendor('azure')

    monkeypatch.setattr(vendor, '__get_azure_ip_ranges__', mock_azure_region_invalid_prefix_data)
    with pytest.raises(NetworkError):
        vendor.fetch()
    assert len(vendor) == 0
