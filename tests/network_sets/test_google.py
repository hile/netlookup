"""
Unit tests for netlookup.whois.network_sets.google module
"""
from netlookup.network_sets.google import GoogleServices


def test_network_sets_google_properties(mock_prefixes_cache):
    """
    Test properties of Google network set properties
    """
    vendor = mock_prefixes_cache.get_vendor('google')
    assert isinstance(vendor, GoogleServices)
