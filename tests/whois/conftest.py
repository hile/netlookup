"""
Unit test configuration for netlookup.whois module
"""
from pathlib import Path

import pytest

from sys_toolkit.tests.mock import MockRunCommandLineOutput

from netlookup.whois.lookup import WhoisAddressLookup
from netlookup.whois.response import WhoisQueryResponse

from ..conftest import MOCK_DATA
from .constants import (
    INVALID_DATETIME_VALUES,
    INVALID_FIELD_VALUES,
    INVALID_WHOIS_RESPONSE_NETWORK_VALUES,
    VALID_DATETIME_VALUES,
    VALID_FIELD_VALUES,
    VALID_WHOIS_RESPONSE_IPRANGE_VALUES,
    VALID_WHOIS_RESPONSE_NETWORK_VALUES,
)

MOCK_ADDRESS_LIST_FILE = MOCK_DATA.joinpath('whois/addresses.txt')
MOCK_QUERY_DOMAIN_FILE = MOCK_DATA.joinpath('whois/domain.txt')
MOCK_QUERY_REVERSE_FILE = MOCK_DATA.joinpath('whois/reverse.txt')


def mock_whois_query_response_data(monkeypatch, path: Path) -> str:
    """
    Mock response data for whois lookup query from text file
    """
    mock_response = MockRunCommandLineOutput(path=path)
    monkeypatch.setattr('netlookup.whois.response.run_command_lineoutput', mock_response)
    return mock_response


@pytest.fixture
def address_list_file():
    """
    Mock returning address list file
    """
    yield MOCK_ADDRESS_LIST_FILE


@pytest.fixture
def mock_whois_address_query(monkeypatch):
    """
    Mock whois query response for MOCK_WHOIS_QUERY_DOMAIN address query
    """
    mock_method = mock_whois_query_response_data(monkeypatch, MOCK_QUERY_REVERSE_FILE)
    return mock_method


@pytest.fixture
def mock_whois_domain_query(monkeypatch):
    """
    Mock whois query response for MOCK_WHOIS_QUERY_DOMAIN domain query
    """
    mock_method = mock_whois_query_response_data(monkeypatch, MOCK_QUERY_DOMAIN_FILE)
    return mock_method


@pytest.fixture
def mock_whois_default_cache(monkeypatch, tmpdir):
    """
    Generate an empty whois query response cache
    """
    cache_file = Path(tmpdir.strpath, 'config/whois.cache')
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
