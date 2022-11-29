"""
Unit test configuration for netlookup module
"""
from http import HTTPStatus
from pathlib import Path
from typing import Optional

import pytest

from dns.resolver import NXDOMAIN
from sys_toolkit.tests.mock import MockCalledMethod, MockException, MockRunCommandLineOutput

from netlookup.network import Network
from netlookup.network_sets.aws import AWS_IP_RANGES_URL
from netlookup.network_sets.cloudflare import CLOUDFLARE_IP_RANGES_IPV4_URL, CLOUDFLARE_IP_RANGES_IPV6_URL
from netlookup.prefixes import Prefixes
from netlookup.whois import PrefixLookup, WhoisLookup

from .constants import (
    GOOGLE_NETWORK_SET_SPF_RECORDS,
    INVALID_NETWORKS,
    NETWORK_ENCODER_OUTPUT_TESTCASES,
    NETWORK_HOST_COUNT_VALUES,
    NETWORK_FIRST_HOST_VALUES,
    NETWORK_LAST_HOST_VALUES,
    NETWORK_PARENT_PREFIX_SIZE_VALUES,
    NETWORK_SUBNET_PREFIX_SIZE_VALUES,
    VALID_NETWORKS,
)
from .utils import create_dns_txt_query_response

MOCK_DATA = Path(__file__).parent.joinpath('mock')

MOCK_AWS_IP_RANGES_FILE = MOCK_DATA.joinpath('network_sets/aws_ip_ranges.json')
MOCK_CLOUDFLARE_V4_RANGES_FILE = MOCK_DATA.joinpath('network_sets/cloudflare_ipv4.txt')
MOCK_CLOUDFLARE_V6_RANGES_FILE = MOCK_DATA.joinpath('network_sets/cloudflare_ipv6.txt')

MOCK_AWS_IP_RANGES_COUNT = 7042
MOCK_CLOUDFLARE_IP_RANGES_COUNT = 22
MOCK_GOOGLE_CLOUD_IP_RANGES_COUNT = 74
MOCK_GOOGLE_SERVICE_IP_RANGES_COUNT = 27

MOCK_PREFIXES_CACHE_DIRECTORY = MOCK_DATA.joinpath('prefixes/cache')
MOCK_PREFIX_LOOKUP_CACHE_FILE = MOCK_DATA.joinpath('whois/pwhois_cache.json')
MOCK_WHOIS_LOOKUP_CACHE_FILE = MOCK_DATA.joinpath('whois/cache.json')


# pylint: disable=too-few-public-methods
class MockGoogleDnsAnswer(MockCalledMethod):
    """
    Mock DNS resolver query answers
    """
    # pylint: disable=arguments-differ
    def __call__(self, record: str, rrtype: str) -> Optional[str]:
        """
        Mock calls to dns.resolver.resolve for google DNS TXT records
        """
        super().__call__(record=record, rrtype=rrtype)
        try:
            record = f'{record.rstrip(".")}.'
            return create_dns_txt_query_response(record, GOOGLE_NETWORK_SET_SPF_RECORDS[record])
        except KeyError as error:
            raise ValueError(f'Unexpected query key: "{record}"') from error


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
def mock_aws_ip_ranges(requests_mock):
    """
    Mock response for AWS IP ranges HTTP request with data from file
    """
    adapter = requests_mock.register_uri(
        'GET',
        AWS_IP_RANGES_URL,
        text=MOCK_AWS_IP_RANGES_FILE.read_text(encoding='UTF-8')
    )
    yield adapter


@pytest.fixture
def mock_aws_ip_ranges_not_found(requests_mock):
    """
    Mock response for AWS IP ranges HTTP request with NOT FOUND HTTP status
    """
    adapter = requests_mock.register_uri(
        'GET',
        AWS_IP_RANGES_URL,
        status_code=HTTPStatus.NOT_FOUND,
    )
    yield adapter


@pytest.fixture
def mock_cloudflare_ip4_ranges(requests_mock):
    """
    Mock response for Cloudflare IPv4 ranges HTTP request with data from file
    """
    adapter = requests_mock.register_uri(
        'GET',
        CLOUDFLARE_IP_RANGES_IPV4_URL,
        text=MOCK_CLOUDFLARE_V4_RANGES_FILE.read_text(encoding='UTF-8')
    )
    yield adapter


@pytest.fixture
def mock_cloudflare_ip4_ranges_not_found(requests_mock):
    """
    Mock response for Cloudflare IPv4 ranges HTTP request with NOT FOUND HTTP status
    """
    adapter = requests_mock.register_uri(
        'GET',
        CLOUDFLARE_IP_RANGES_IPV4_URL,
        status_code=HTTPStatus.NOT_FOUND,
    )
    yield adapter


@pytest.fixture
def mock_cloudflare_ip6_ranges(requests_mock):
    """
    Mock response for Cloudflare IPv4 ranges HTTP request with data from file
    """
    adapter = requests_mock.register_uri(
        'GET',
        CLOUDFLARE_IP_RANGES_IPV6_URL,
        text=MOCK_CLOUDFLARE_V6_RANGES_FILE.read_text(encoding='UTF-8')
    )
    yield adapter


@pytest.fixture
def mock_cloudflare_ip6_ranges_not_found(requests_mock):
    """
    Mock response for Cloudflare IPv6 ranges HTTP request with NOT FOUND HTTP status
    """
    adapter = requests_mock.register_uri(
        'GET',
        CLOUDFLARE_IP_RANGES_IPV6_URL,
        status_code=HTTPStatus.NOT_FOUND,
    )
    yield adapter


@pytest.fixture
def mock_google_dns_requests(monkeypatch):
    """
    Mock responses to Google DNS queries
    """
    mock_answer = MockGoogleDnsAnswer()
    monkeypatch.setattr('netlookup.network_sets.google.resolver.resolve', mock_answer)
    return mock_answer


@pytest.fixture
def mock_google_dns_requests_error(monkeypatch):
    """
    Mock error raised for responses to Google DNS queries
    """
    mock_error = MockException(NXDOMAIN)
    monkeypatch.setattr('netlookup.network_sets.google.resolver.resolve', mock_error)
    return mock_error


@pytest.fixture
def mock_prefixes_cache_empty(tmpdir):
    """
    Return prefixes object with cache path from mocked data
    """
    yield Prefixes(cache_directory=tmpdir.strpath)


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
