"""
Unnit tests for netlookup.prefixes cloud address pool parsing
"""
import tempfile

import pytest

from netlookup.network import NetworkError
from netlookup.prefixes import Prefixes

INVALID_URL = 'http://tuohela.net/invalid-url-test'


def mock_invalid_json_data():
    """
    Mock invalid data string not in JSON format
    """
    return '{"invalid"}'


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
