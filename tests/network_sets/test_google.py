#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.network_sets.google module
"""
import pytest

from netlookup.exceptions import NetworkError
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
    Test updating google cloud network sets with mocked DNS response data
    """
    google_cloud_prefixes = mock_prefixes_cache_empty.get_vendor('google-cloud')
    assert len(google_cloud_prefixes) == 0
    google_cloud_prefixes.fetch()
    assert len(google_cloud_prefixes) == MOCK_GOOGLE_CLOUD_IP_RANGES_COUNT


# pylint: disable=unused-argument
def test_network_sets_google_cloud_update_error(
        mock_prefixes_cache_empty,
        mock_google_dns_requests_error) -> None:
    """
    Test updating google cloud network sets with NXDOMAIN error
    """
    google_cloud_prefixes = mock_prefixes_cache_empty.get_vendor('google-cloud')
    with pytest.raises(NetworkError):
        google_cloud_prefixes.fetch()


# pylint: disable=unused-argument
def test_network_sets_google_services_update(
        mock_prefixes_cache_empty,
        mock_google_dns_requests) -> None:
    """
    Test updating google services network sets with mocked DNS response data
    """
    google_services_prefixes = mock_prefixes_cache_empty.get_vendor('google')
    assert len(google_services_prefixes) == 0
    google_services_prefixes.fetch()
    assert len(google_services_prefixes) == MOCK_GOOGLE_SERVICE_IP_RANGES_COUNT


# pylint: disable=unused-argument
def test_network_sets_google_services_update_error(
        mock_prefixes_cache_empty,
        mock_google_dns_requests_error) -> None:
    """
    Test updating google services network sets with NXDOMAIN error
    """
    google_services_prefixes = mock_prefixes_cache_empty.get_vendor('google')
    with pytest.raises(NetworkError):
        google_services_prefixes.fetch()
