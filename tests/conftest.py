"""
Unit test configuration for netlookup module
"""
from pathlib import Path

import pytest

from sys_toolkit.tests.mock import MockRunCommandLineOutput

from netlookup.network import Network
from netlookup.prefixes import Prefixes
from netlookup.whois import PrefixLookup, WhoisLookup

from .constants import (
    INVALID_NETWORKS,
    NETWORK_ENCODER_OUTPUT_TESTCASES,
    NETWORK_HOST_COUNT_VALUES,
    NETWORK_FIRST_HOST_VALUES,
    NETWORK_LAST_HOST_VALUES,
    NETWORK_PARENT_PREFIX_SIZE_VALUES,
    NETWORK_SUBNET_PREFIX_SIZE_VALUES,
    VALID_NETWORKS,
)

MOCK_DATA = Path(__file__).parent.joinpath('mock')
MOCK_PREFIXES_CACHE_DIRECTORY = MOCK_DATA.joinpath('prefixes/cache')
MOCK_PREFIX_LOOKUP_CACHE_FILE = MOCK_DATA.joinpath('whois/pwhois_cache.json')
MOCK_WHOIS_LOOKUP_CACHE_FILE = MOCK_DATA.joinpath('whois/cache.json')


def mock_platform(monkeypatch, platform: str):
    """
    Mock sys.platform value for specified environment
    """
    monkeypatch.setattr('sys.platform', platform)


def mock_environment_services(monkeypatch, environment):
    """
    Mock loading of environment's /etc/services from mock data
    """
    monkeypatch.setattr(
        'netlookup.services.SERVICES_FILE_PATH',
        str(MOCK_DATA.joinpath(f'platform/{environment}/services'))
    )


def mock_environment_protocols(monkeypatch, environment):
    """
    Mock loading of environment's /etc/protocols from mock data
    """
    monkeypatch.setattr(
        'netlookup.protocols.PROTOCOLS_FILE_PATH',
        str(MOCK_DATA.joinpath(f'platform/{environment}/protocols'))
    )


@pytest.fixture
def mock_prefixes_cache() -> Prefixes:
    """
    Return prefixes object with cache path from mocked data
    """
    yield Prefixes(cache_directory=MOCK_PREFIXES_CACHE_DIRECTORY)


@pytest.fixture
def mock_whois_query_no_data(monkeypatch) -> str:
    """
    Mock query for whois query to return no data
    """
    mock_response = MockRunCommandLineOutput(stdout='', stderr='')
    monkeypatch.setattr('netlookup.whois.response.run_command_lineoutput', mock_response)
    return mock_response


@pytest.fixture
def mock_whois_lookup_cache() -> WhoisLookup:
    """
    Return whois address lookup object with cache file from mocked data
    """
    yield WhoisLookup(cache_file=MOCK_WHOIS_LOOKUP_CACHE_FILE)


@pytest.fixture
def mock_prefix_lookup_cache() -> PrefixLookup:
    """
    Return prefix address lookup object with cache file from mocked data
    """
    yield PrefixLookup(cache_file=MOCK_PREFIX_LOOKUP_CACHE_FILE)


@pytest.fixture
def mock_darwin_files(monkeypatch):
    """
    Mock loading of /etc/services and /etc/platforms for macOS darwin
    """
    mock_environment_protocols(monkeypatch, 'darwin')
    mock_environment_services(monkeypatch, 'darwin')


@pytest.fixture
def mock_freebsd_files(monkeypatch):
    """
    Mock loading of /etc/services and /etc/platforms for FreeBSD
    """
    mock_environment_protocols(monkeypatch, 'freebsd')
    mock_environment_services(monkeypatch, 'freebsd')


@pytest.fixture
def mock_linux_files(monkeypatch):
    """
    Mock loading of /etc/services and /etc/platforms for Linux
    """
    mock_environment_protocols(monkeypatch, 'linux')
    mock_environment_services(monkeypatch, 'linux')


@pytest.fixture
def mock_openbsd_files(monkeypatch):
    """
    Mock loading of /etc/services and /etc/platforms for OpenBSD
    """
    mock_environment_protocols(monkeypatch, 'openbsd')
    mock_environment_services(monkeypatch, 'openbsd')


@pytest.fixture(params=NETWORK_ENCODER_OUTPUT_TESTCASES)
def network_encoder_output(request):
    """
    Generate list of invalid networks
    """
    yield request.param


@pytest.fixture(params=INVALID_NETWORKS)
def invalid_network(request):
    """
    Generate list of invalid networks
    """
    yield request.param


@pytest.fixture(params=VALID_NETWORKS)
def valid_network(request):
    """
    Generate list of valid networks
    """
    yield request.param


@pytest.fixture
def valid_network_list():
    """
    Return list of network objects
    """
    yield [Network(value) for value in VALID_NETWORKS]


@pytest.fixture(params=NETWORK_HOST_COUNT_VALUES)
def network_host_count_value(request):
    """
    Generate network, subnet host count value tuples
    """
    yield request.param


@pytest.fixture(params=NETWORK_FIRST_HOST_VALUES)
def network_first_host_tuple(request):
    """
    Generate network, first host value value tuples
    """
    yield request.param


@pytest.fixture(params=NETWORK_LAST_HOST_VALUES)
def network_last_host_tuple(request):
    """
    Generate network, last host value value tuples
    """
    yield request.param


@pytest.fixture(params=NETWORK_PARENT_PREFIX_SIZE_VALUES)
def network_parent_prefix_size(request):
    """
    Generate network, parent prefix size value tuples
    """
    yield request.param


@pytest.fixture(params=NETWORK_SUBNET_PREFIX_SIZE_VALUES)
def network_subnet_prefix_size(request):
    """
    Generate network, subnet prefix size value tuples
    """
    yield request.param
