"""
Unit test constants for netlookup module
"""
from netaddr.ip import IPAddress

# Number of items in mock/prefixes/cache directory data
MOCK_PREFIXES_CACHE_LEN = 1511

# Valid network values for unit testing
VALID_NETWORKS = (
    '127.0.0.1',
    '10.0.0.0/32',
    '::1',
    '::1/128',
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
    ('192.168.64.65/31', IPAddress('192.168.64.64')),
    ('192.168.64.65/32', None),
    ('2001::1/127', IPAddress('2001::0')),
    ('2001::1/128', None),
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
