"""
Unit test configuration for netlookup.whois module
"""
from pathlib import Path

import pytest

from netlookup.whois.lookup import WhoisAddressLookup
from netlookup.whois.response import WhoisQueryResponse

from .constants import (
    INVALID_DATETIME_VALUES,
    INVALID_FIELD_VALUES,
    INVALID_WHOIS_RESPONSE_NETWORK_VALUES,
    VALID_DATETIME_VALUES,
    VALID_FIELD_VALUES,
    VALID_WHOIS_RESPONSE_IPRANGE_VALUES,
    VALID_WHOIS_RESPONSE_NETWORK_VALUES,
)


@pytest.fixture
def mock_whois_default_cache(monkeypatch, tmpdir):
    """
    Generate an empty whois query response cache
    """
    cache_file = Path(tmpdir.strpath, 'whois.cache')
    monkeypatch.setattr('netlookup.whois.lookup.WHOIS_CACHE_FILE', cache_file)
    yield cache_file


# pylint: disable=redefined-outer-name
@pytest.fixture
def empty_whois_query_cache(mock_whois_default_cache):
    """
    Generate an empty whois query response cache
    """
    yield WhoisAddressLookup(cache_file=mock_whois_default_cache)


@pytest.fixture
def empty_whois_response():
    """
    Generate an empty whois response for unit tests
    """
    yield WhoisQueryResponse(WhoisAddressLookup())


@pytest.fixture(params=INVALID_DATETIME_VALUES)
def invalid_datetime_value(request):
    """
    Generate invalid datetime values for unit tests
    """
    yield request.param


@pytest.fixture(params=VALID_DATETIME_VALUES)
def valid_datetime_value(request):
    """
    Generate invalid datetime values for unit tests
    """
    yield request.param


@pytest.fixture(params=INVALID_FIELD_VALUES)
def invalid_field_value(request):
    """
    Generate invalid field values for unit tests
    """
    yield request.param


@pytest.fixture(params=VALID_FIELD_VALUES)
def valid_field_value(request):
    """
    Generate valid field values for unit tests
    """
    yield request.param


@pytest.fixture(params=INVALID_WHOIS_RESPONSE_NETWORK_VALUES)
def invalid_whois_network_value(request):
    """
    Generate invalid whois response network values for unit tests
    """
    yield request.param


@pytest.fixture(params=VALID_WHOIS_RESPONSE_IPRANGE_VALUES)
def valid_whois_iprange_value(request):
    """
    Generate valid whois response IP range values for unit tests
    """
    yield request.param


@pytest.fixture(params=VALID_WHOIS_RESPONSE_NETWORK_VALUES)
def valid_whois_networks_value(request):
    """
    Generate valid whois response network values for unit tests
    """
    yield request.param
