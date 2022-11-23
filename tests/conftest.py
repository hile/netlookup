"""
Unit test settings
"""

from pathlib import Path

import pytest

MOCK_DATA = Path(__file__).parent.joinpath('mock')

MOCK_PREFIX_CACHE_PATH = MOCK_DATA.joinpath('prefixes')
INVALID_JSON_CACHE_FILE = MOCK_PREFIX_CACHE_PATH.joinpath('invalid_json_data.json')
INVALID_NETWORK_SET_CACHE_FILE = MOCK_PREFIX_CACHE_PATH.joinpath('invalid_network_set.json')
SUBSTRACT_CACHE_FILE = MOCK_PREFIX_CACHE_PATH.joinpath('substract_networks.json')

VALID_SUBNET_VALUES = (
    '10.0.0.0/8',
    '2c0f:fb50:4000::/36',
    '2c0f:fb50:5000::',
)

VALID_ADDRESS_LOOKUPS = (
    '10.0.0.0',
    '10.1.2.3',
    '2c0f:fb50:4000::0',
    '2c0f:fb50:4000::123',
)

# Invalid values for subnets
INVALID_SUBNET_VALUES = (
    '0.0.0.0/33',
    '10.0.0.256/32',
    '2c0f:fb50:4000::/',
    '2c0f:fb50:4000::/129',
)

# How many times we may try splitting
MAX_SPLITS = 8

# Values for address lookups that match prefixes in test data
MATCH_PREFIXES_LOOKUPS = (
    '107.167.164.19',
    '2600:1900::abba:dead:beef',
)

# Values not valid for IPAddress lookups
INVALID_ADDRESS_LOOKUPS = (
    'foobar',
    'example.com',
)


@pytest.fixture(autouse=True)
def mock_whois_cache_path(monkeypatch, tmpdir):
    """
    Mock whois cache file path to avoid using existing caches
    """
    print('mock whois lookup cache file')
    monkeypatch.setattr(
        'netlookup.whois.lookup.WHOIS_CACHE_FILE',
        Path(tmpdir, 'whois.json')
    )
