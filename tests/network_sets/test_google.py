"""
Unit tests for netlookup.whois.network_sets.google module
"""
from netlookup.network_sets.google import GoogleCloud, GoogleServices

from .common import validate_network_set_properties
from ..conftest import MOCK_GOOGLE_CLOUD_IP_RANGES_COUNT, MOCK_GOOGLE_SERVICE_IP_RANGES_COUNT


def test_network_sets_google_properties(mock_prefixes_cache) -> None:
    """
    Test properties of Google network set properties
    """
    validate_network_set_properties(mock_prefixes_cache.get_vendor('google'), GoogleServices)


def test_network_sets_google_cloud_properties(mock_prefixes_cache) -> None:
    """
    Test properties of Google Cloud network set properties
    """
    validate_network_set_properties(mock_prefixes_cache.get_vendor('google-cloud'), GoogleCloud)


# pylint: disable=unused-argument
def test_network_sets_google_cloud_update(
        mock_prefixes_cache_empty,
        mock_google_dns_requests) -> None:
    """
    Test updating google services network sets with mocked DNS response data
    """
    google_cloud_prefixes = mock_prefixes_cache_empty.get_vendor('google-cloud')
    assert len(google_cloud_prefixes.__networks__) == 0
    google_cloud_prefixes.fetch()
    assert len(google_cloud_prefixes.__networks__) == MOCK_GOOGLE_CLOUD_IP_RANGES_COUNT


# pylint: disable=unused-argument
def test_network_sets_google_services_update(
        mock_prefixes_cache_empty,
        mock_google_dns_requests) -> None:
    """
    Test updating google services network sets with mocked DNS response data
    """
    google_services_prefixes = mock_prefixes_cache_empty.get_vendor('google')
    assert len(google_services_prefixes.__networks__) == 0
    google_services_prefixes.fetch()
    assert len(google_services_prefixes.__networks__) == MOCK_GOOGLE_SERVICE_IP_RANGES_COUNT
