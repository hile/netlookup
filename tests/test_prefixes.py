"""
Unit tests for netlookup.prefixes module
"""
from netlookup.prefixes import Prefixes

from .constants import MOCK_PREFIXES_CACHE_LEN, MOCK_PREFIXES_DATA_LEN


def test_prefixes_cache_load(mock_prefixes_cache) -> None:
    """
    Test loading cached prefixes from mocked data, ensure the number of
    prefixes is correct
    """
    prefixes = mock_prefixes_cache
    assert isinstance(prefixes, Prefixes)
    assert len(prefixes) == MOCK_PREFIXES_CACHE_LEN


# pylint: disable=unused-argument
def test_prefixes_cache_properties_update(
        mock_prefixes_cache_empty,
        mock_aws_ip_ranges,
        mock_cloudflare_ip4_ranges,
        mock_cloudflare_ip6_ranges,
        mock_google_dns_requests):
    """
    Test updating prefixes cache with mocked data
    """
    prefixes = mock_prefixes_cache_empty
    assert len(prefixes) == 0
    prefixes.update()
    assert len(prefixes) == MOCK_PREFIXES_DATA_LEN

    for prefix in prefixes:
        assert isinstance(prefix.__repr__(), str)
        assert isinstance(prefix.__str__(), str)
