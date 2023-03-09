#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.prefixes module
"""
from shutil import rmtree

import pytest

from netlookup.exceptions import NetworkError
from netlookup.prefixes import Prefixes
from netlookup.network_sets.google import GoogleCloudPrefix, GoogleServicePrefix

from .constants import (
    MOCK_PREFIXES_CACHE_LEN,
    MOCK_PREFIXES_DATA_LEN,
    PREFIXES_GOOGLE_CLOUD_MATCH,
    PREFIXES_GOOGLE_SERVICES_MATCH,
)
from .network_sets.test_aws import MOCK_AWS_IP_RANGES_COUNT
from .network_sets.test_cloudflare import MOCK_CLOUDFLARE_IP_RANGES_COUNT
from .network_sets.test_google import MOCK_GOOGLE_CLOUD_IP_RANGES_COUNT, MOCK_GOOGLE_SERVICE_IP_RANGES_COUNT

INVALID_VENDOR = 'invalid-vendor-name'


def test_prefixes_cache_load(mock_prefixes_cache) -> None:
    """
    Test loading cached prefixes from mocked data, ensure the number of
    prefixes is correct
    """
    prefixes = mock_prefixes_cache
    assert isinstance(prefixes, Prefixes)
    assert len(prefixes) == MOCK_PREFIXES_CACHE_LEN


# pylint: disable=unused-argument
def test_prefixes_load_missing_directory_permission_denied(
        mock_prefixes_cache_directory_missing_permission_denied) -> None:
    """
    Test loading prefixes with cache path missing and pointing to a directory that can't be created
    """
    assert not mock_prefixes_cache_directory_missing_permission_denied.exists()
    with pytest.raises(NetworkError):
        Prefixes(cache_directory=mock_prefixes_cache_directory_missing_permission_denied)

    # For some reason cleanup can't do this in teardown
    if mock_prefixes_cache_directory_missing_permission_denied.parent.is_dir():
        mock_prefixes_cache_directory_missing_permission_denied.parent.chmod(int('0700', 8))


# pylint: disable=unused-argument
def test_prefixes_load_and_save_missing_directory(
        mock_prefixes_cache_directory_missing,
        mock_aws_ip_ranges,
        mock_cloudflare_ip4_ranges,
        mock_cloudflare_ip6_ranges,
        mock_google_dns_requests) -> None:
    """
    Test find with missing cache directory, updating and saving new data files
    """
    assert not mock_prefixes_cache_directory_missing.is_dir()
    prefixes = Prefixes(cache_directory=mock_prefixes_cache_directory_missing)
    assert prefixes.cache_directory == mock_prefixes_cache_directory_missing
    assert mock_prefixes_cache_directory_missing.is_dir()

    prefixes.update()
    prefixes.save()

    assert len(prefixes.filter_type('aws')) == MOCK_AWS_IP_RANGES_COUNT
    assert len(prefixes.filter_type('cloudflare')) == MOCK_CLOUDFLARE_IP_RANGES_COUNT
    assert len(prefixes.filter_type('google-cloud')) == MOCK_GOOGLE_CLOUD_IP_RANGES_COUNT
    assert len(prefixes.filter_type('google')) == MOCK_GOOGLE_SERVICE_IP_RANGES_COUNT


def test_prefixes_load_cache_file_invalid_json(mock_prefixes_cache_invalid_json_data) -> None:
    """
    Test find with cache files that are not valid JSON objects
    """
    with pytest.raises(NetworkError):
        Prefixes(cache_directory=mock_prefixes_cache_invalid_json_data)


def test_prefixes_load_cache_file_invalid_address_data(mock_prefixes_cache_invalid_address_data) -> None:
    """
    Test find with cache files that are not valid address objects
    """
    with pytest.raises(NetworkError):
        Prefixes(cache_directory=mock_prefixes_cache_invalid_address_data)


def test_prefixes_load_cache_file_error(mock_prefixes_cache_permission_denied) -> None:
    """
    Test find with cache files that have no read permissions
    """
    with pytest.raises(NetworkError):
        Prefixes(cache_directory=mock_prefixes_cache_permission_denied)


# pylint: disable=unused-argument
def test_prefixes_cache_properties_update(
        mock_prefixes_cache_empty,
        mock_aws_ip_ranges,
        mock_cloudflare_ip4_ranges,
        mock_cloudflare_ip6_ranges,
        mock_google_dns_requests) -> None:
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


# pylint: disable=unused-argument
def test_prefixes_cache_properties_update_permission_denied(
        mock_prefixes_cache_directory_missing,
        mock_aws_ip_ranges,
        mock_cloudflare_ip4_ranges,
        mock_cloudflare_ip6_ranges,
        mock_google_dns_requests) -> None:
    """
    Test updating prefixes cache with mocked data and a non-writable cache directory
    """
    prefixes = Prefixes(cache_directory=mock_prefixes_cache_directory_missing)
    rmtree(prefixes.cache_directory)
    with pytest.raises(NetworkError):
        prefixes.save()


# pylint: disable=unused-argument
def test_prefixes_cache_properties_update_save_error(
        mock_prefixes_cache_directory_missing,
        mock_network_set_save_error,
        mock_aws_ip_ranges,
        mock_cloudflare_ip4_ranges,
        mock_cloudflare_ip6_ranges,
        mock_google_dns_requests) -> None:
    """
    Test updating prefixes cache with mocked data and an error from network set save method
    """
    prefixes = Prefixes(cache_directory=mock_prefixes_cache_directory_missing)
    with pytest.raises(NetworkError):
        prefixes.update()


def test_prefixes_cache_get_vendor_invalid(mock_prefixes_cache) -> None:
    """
    Test handling of getting get_vendor with unexpected vendor name
    """
    with pytest.raises(NetworkError):
        mock_prefixes_cache.get_vendor(INVALID_VENDOR)


def test_prefixes_cache_find_google_cloud_address(mock_prefixes_cache) -> None:
    """
    Test find with a network in cache
    """
    network = mock_prefixes_cache.find(PREFIXES_GOOGLE_CLOUD_MATCH)
    assert isinstance(network, GoogleCloudPrefix)


def test_prefixes_cache_find_google_services_address(mock_prefixes_cache) -> None:
    """
    Test find with a network in cache
    """
    network = mock_prefixes_cache.find(PREFIXES_GOOGLE_SERVICES_MATCH)
    assert isinstance(network, GoogleServicePrefix)
