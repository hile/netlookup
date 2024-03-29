#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.network_sets.aws module
"""
import pytest

from netlookup.exceptions import NetworkError
from netlookup.network_sets.aws import AWS

from ..conftest import MOCK_AWS_IP_RANGES_COUNT
from .common import validate_network_set_properties

VENDOR = 'aws'


def test_network_sets_aws_properties(mock_prefixes_cache) -> None:
    """
    Test properties of AWS network set
    """
    validate_network_set_properties(mock_prefixes_cache.get_vendor(VENDOR), AWS)


# pylint: disable=unused-argument
def test_network_sets_aws_update_http_error(mock_prefixes_cache_empty, mock_aws_ip_ranges_not_found) -> None:
    """
    Test updating the AWS network with empty cache and HTTP error code
    """
    aws = mock_prefixes_cache_empty.get_vendor(VENDOR)
    assert len(aws) == 0
    with pytest.raises(NetworkError):
        aws.fetch()
    assert len(aws) == 0

    assert len(mock_prefixes_cache_empty.filter_type(VENDOR)) == 0


# pylint: disable=unused-argument
def test_network_sets_aws_update(mock_prefixes_cache_empty, mock_aws_ip_ranges) -> None:
    """
    Test updating the AWS network with empty cache
    """
    aws = mock_prefixes_cache_empty.get_vendor(VENDOR)
    assert len(aws) == 0
    aws.fetch()
    assert len(aws) == MOCK_AWS_IP_RANGES_COUNT
    for network in aws:
        assert isinstance(network.__repr__(), str)

    assert isinstance(aws.regions, list)
    assert len(aws.regions) > 0
    for region in aws.regions:
        assert isinstance(region, str)
