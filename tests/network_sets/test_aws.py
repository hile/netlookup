"""
Unit tests for netlookup.whois.network_sets.aws module
"""

from netlookup.network_sets.aws import AWS


def test_network_sets_aws_properties(mock_prefixes_cache):
    """
    Test properties of AWS network set
    """
    vendor = mock_prefixes_cache.get_vendor('aws')
    assert isinstance(vendor, AWS)
