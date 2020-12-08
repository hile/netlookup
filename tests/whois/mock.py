"""
Mock loaders for whois test data
"""

from pathlib import Path

from netlookup.whois.lookup import WhoisAddressLookup
from netlookup.whois.response import WhoisQueryResponse

TEST_DATA = Path(__file__).parent.joinpath('data')
TEST_INETNUM_LINE = 'inetnum: 1.2.3.0 - 1.2.3.255'

TEST_CACHE = TEST_DATA.joinpath('cache.json')
TEST_CACHE_SIZE = 164


def load_test_file_lines(path):
    """
    Load test file as lines
    """
    with path.open('r') as filedescriptor:
        return filedescriptor.readlines()


def get_empty_response():
    """
    Return empty WhoisQueryResponse object
    """
    return WhoisQueryResponse(WhoisAddressLookup())


def get_test_reverse_lines():
    """
    Get lines for test reverse record
    """
    return load_test_file_lines(TEST_DATA.joinpath('reverse.txt'))


def get_test_domain_lines():
    """
    Get lines for test domain record
    """
    return load_test_file_lines(TEST_DATA.joinpath('domain.txt'))
