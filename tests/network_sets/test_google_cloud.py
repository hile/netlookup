"""
Unit tests for netlookup.whois.network_sets.gcp module
"""
from netlookup.network_sets.google_cloud import GoogleCloud


def test_network_sets_google_cloud_properties(mock_prefixes_cache):
    """
    Test properties of Google Cloud network set properties
    """
    vendor = mock_prefixes_cache.get_vendor('google-cloud')
    assert isinstance(vendor, GoogleCloud)
