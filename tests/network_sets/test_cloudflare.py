"""
Unit tests for netlookup.whois.network_sets.cloudflare module
"""
import pytest

from netlookup.exceptions import NetworkError
from netlookup.network_sets.cloudflare import Cloudflare

from ..conftest import MOCK_CLOUDFLARE_IP_RANGES_COUNT
from .common import validate_network_set_properties


def test_network_sets_cloudflare_properties(mock_prefixes_cache) -> None:
    """
    Test properties of Cloudflare network set
    """
    validate_network_set_properties(mock_prefixes_cache.get_vendor('cloudflare'), Cloudflare)


# pylint: disable=unused-argument
def test_network_sets_cloudflare_update_ipv4_http_error(
        mock_prefixes_cache_empty,
        mock_cloudflare_ip4_ranges_not_found) -> None:
    """
    Test updating the Cloudflare network with empty cache and HTTP error code from IPv4 address file
    """
    cloudflare = mock_prefixes_cache_empty.get_vendor('cloudflare')
    assert len(cloudflare) == 0
    with pytest.raises(NetworkError):
        cloudflare.fetch()
    assert len(cloudflare) == 0


# pylint: disable=unused-argument
def test_network_sets_cloudflare_update_ipv6_http_error(
        mock_prefixes_cache_empty,
        mock_cloudflare_ip6_ranges_not_found) -> None:
    """
    Test updating the Cloudflare network with empty cache and HTTP error code from IPv6 address file
    """
    cloudflare = mock_prefixes_cache_empty.get_vendor('cloudflare')
    assert len(cloudflare) == 0
    with pytest.raises(NetworkError):
        cloudflare.fetch()
    assert len(cloudflare) == 0


# pylint: disable=unused-argument
def test_network_sets_cloudflare_update(
        mock_prefixes_cache_empty,
        mock_cloudflare_ip4_ranges,
        mock_cloudflare_ip6_ranges) -> None:
    """
    Test updating the AWS network with empty cache
    """
    cloudflare = mock_prefixes_cache_empty.get_vendor('cloudflare')
    assert len(cloudflare) == 0
    cloudflare.fetch()
    assert len(cloudflare) == MOCK_CLOUDFLARE_IP_RANGES_COUNT
    for network in cloudflare:
        assert isinstance(network.__repr__(), str)
