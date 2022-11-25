"""
Unit test constants for netlookup module
"""
from datetime import datetime, timezone
from netaddr.ip import IPAddress, IPNetwork, IPRange

# How many times we may try splitting
MAX_SPLITS = 8

# Number of items in mock/prefixes/cache directory data
MOCK_PREFIXES_CACHE_LEN = 1511

# Valid network values for unit testing
VALID_NETWORKS = (
    '127.0.0.1',
    '10.0.0.0/32',
    '::1',
    '::1/128',
    '192.168.64.0/24',
    'fe80::6cfa:48ff:fe2e:fd18',
    '2001:14ba:3e9::/64',
    '2c0f:fb50:4000::/36',
    '2c0f:fb50:5000::',
)

INVALID_NETWORKS = (
    '',
    'foobar',
    'example.com',
    '192.168.3.256/24',
    '192.168.3.0/33',
)

# List of 'network, first host' pairs for unit tests
NETWORK_FIRST_HOST_VALUES = (
    ('192.168.64.0/24', IPAddress('192.168.64.1')),
    ('192.168.64.65/31', IPAddress('192.168.64.64')),
    ('192.168.64.65/32', None),
    ('2001:14ba:3e7:8303:2086:ca84:dbad:b4f2/64', IPAddress('2001:14ba:3e7:8303::1')),
    ('2001::1/127', IPAddress('2001::0')),
    ('2001::1/128', None),
)

# List of 'network, last host' pairs for unit tests
NETWORK_HOST_COUNT_VALUES = (
    ('192.168.64.65/32', 1),
    ('2001::1/128', 1),
    ('192.168.64.65/31', 2),
    ('2001::1/127', 2),
    ('192.168.8.96/15', 131070),
    ('2001:999:61:2660:2950::/64', 18446744073709551614),
)

# List of 'network, last host' pairs for unit tests
NETWORK_LAST_HOST_VALUES = (
    ('192.168.64.65/32', None),
    ('2001::1/128', None),
    ('192.168.64.65/31', IPAddress('192.168.64.65')),
    ('2001::1/127', IPAddress('2001::1')),
    ('192.168.8.96/15', IPAddress('192.169.255.254')),
    ('2001:999:61:2660:2950::/64', IPAddress('2001:999:61:2660:ffff:ffff:ffff:fffe')),
)

# JSON encoder output test cases for netlookup.encoders.NetworkDataEncoder
NETWORK_ENCODER_OUTPUT_TESTCASES = (
    (IPAddress('192.168.64.65'), '"192.168.64.65"'),
    (IPNetwork('192.168.64.0/24'), '"192.168.64.0/24"'),
    (IPRange('192.168.64.1', '192.168.64.5'), '"192.168.64.1-192.168.64.5"'),
    ({'a': 1, 'b': 2}, '{"a": 1, "b": 2}'),
    (
        datetime(year=2001, month=1, day=14, minute=14, tzinfo=timezone.utc),
        '"2001-01-14T00:14:00+00:00"'
    ),
    (123, '123'),
    (False, 'false'),
)
