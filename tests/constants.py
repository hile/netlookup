#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit test constants for netlookup module
"""
from datetime import datetime, timezone
from netaddr.ip import IPAddress, IPNetwork, IPRange

# How many times we may try splitting
MAX_SPLITS = 8

# Number of items in mock/prefixes/cache directory data
MOCK_PREFIXES_CACHE_LEN = 1533

# Number of prefixes when all caches are loaded from APIs
MOCK_PREFIXES_DATA_LEN = 7165

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

SPLITTABLE_NETWORKS = (
    '192.168.64.0/24',
    '2001:14ba:3e9::/64',
    '2c0f:fb50:4000::/36',
)
UNSPLITTABLE_NETWORKS = (
    '127.0.0.1',
    '10.0.0.0/32',
    '::1',
    '::1/128',
)

INVALID_NETWORKS = (
    '',
    'foobar',
    'example.com',
    '192.168.3.256/24',
    '192.168.3.0/33',
)

# List of 'network, parent prefix' pairs for unit tests
NETWORK_PARENT_PREFIX_SIZE_VALUES = (
    ('0.0.0.0/0', None),
    ('192.168.64.65/32', 31),
    ('2001::1/128', 127),
    ('1.2.3.4/18', 17),
    ('2001::1/48', 47),
)

# List of 'network, parent prefix' pairs for unit tests
NETWORK_SUBNET_PREFIX_SIZE_VALUES = (
    ('255.255.255.255', None),
    ('192.168.64.65/32', None),
    ('2001::1/128', None),
    ('1.2.3.4/18', 19),
    ('2001::1/48', 49),
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
NETWORK_LAST_HOST_VALUES = (
    ('192.168.64.65/32', None),
    ('2001::1/128', None),
    ('192.168.64.65/31', IPAddress('192.168.64.65')),
    ('2001::1/127', IPAddress('2001::1')),
    ('192.168.8.96/15', IPAddress('192.169.255.254')),
    ('2001:999:61:2660:2950::/64', IPAddress('2001:999:61:2660:ffff:ffff:ffff:fffe')),
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

PREFIXES_NO_MATCH = '255.254.252.251'
PREFIXES_GOOGLE_SERVICES_MATCH = '2800:3f0:4004::123'
PREFIXES_GOOGLE_CLOUD_MATCH = '8.34.210.5'

# SPF records for google services and google cloud as of November 2022
GOOGLE_NETWORK_SET_SPF_RECORDS = {
    '_cloud-netblocks.googleusercontent.com.': (
        'v=spf1',
        'include:_cloud-netblocks1.googleusercontent.com',
        'include:_cloud-netblocks2.googleusercontent.com',
        'include:_cloud-netblocks3.googleusercontent.com',
        'include:_cloud-netblocks4.googleusercontent.com',
        'include:_cloud-netblocks5.googleusercontent.com',
        '?all'
    ),
    '_cloud-netblocks1.googleusercontent.com.': (
        'v=spf1',
        'include:_cloud-netblocks6.googleusercontent.com',
        'include:_cloud-netblocks7.googleusercontent.com',
        'ip6:2600:1900::/35',
        'ip4:8.34.208.0/20',
        'ip4:8.35.192.0/21',
        'ip4:8.35.200.0/23',
        'ip4:23.236.48.0/20',
        'ip4:23.251.128.0/19',
        'ip4:34.64.0.0/11',
        'ip4:34.96.0.0/14',
        '?all',
    ),
    '_cloud-netblocks2.googleusercontent.com.': (
        'v=spf1',
        'ip4:34.100.0.0/16',
        'ip4:34.102.0.0/15',
        'ip4:34.104.0.0/14',
        'ip4:34.124.0.0/18',
        'ip4:34.124.64.0/20',
        'ip4:34.124.80.0/23',
        'ip4:34.124.84.0/22',
        'ip4:34.124.88.0/23',
        'ip4:34.124.92.0/22',
        'ip4:34.125.0.0/16',
        'ip4:35.184.0.0/14',
        'ip4:35.188.0.0/15',
        'ip4:35.190.0.0/17',
        '?all'
    ),
    '_cloud-netblocks3.googleusercontent.com.': (
        'v=spf1',
        'ip4:35.190.128.0/18',
        'ip4:35.190.192.0/19',
        'ip4:35.190.224.0/20',
        'ip4:35.190.240.0/22',
        'ip4:35.192.0.0/14',
        'ip4:35.196.0.0/15',
        'ip4:35.198.0.0/16',
        'ip4:35.199.0.0/17',
        'ip4:35.199.128.0/18',
        'ip4:35.200.0.0/13',
        'ip4:35.208.0.0/13',
        'ip4:35.216.0.0/15',
        '?all'
    ),
    '_cloud-netblocks4.googleusercontent.com.': (
        'v=spf1',
        'ip4:35.219.192.0/24',
        'ip4:35.220.0.0/14',
        'ip4:35.224.0.0/13',
        'ip4:35.232.0.0/15',
        'ip4:35.234.0.0/16',
        'ip4:35.235.0.0/17',
        'ip4:35.235.192.0/20',
        'ip4:35.235.216.0/21',
        'ip4:35.235.224.0/20',
        'ip4:35.236.0.0/14',
        'ip4:35.240.0.0/13',
        'ip4:104.154.0.0/15',
        'ip4:104.196.0.0/14',
        '?all'
    ),
    '_cloud-netblocks5.googleusercontent.com.': (
        'v=spf1',
        'ip4:107.167.160.0/19',
        'ip4:107.178.192.0/18',
        'ip4:108.59.80.0/20',
        'ip4:108.170.192.0/20',
        'ip4:108.170.208.0/21',
        'ip4:108.170.216.0/22',
        'ip4:108.170.220.0/23',
        'ip4:108.170.222.0/24',
        'ip4:130.211.4.0/22',
        'ip4:130.211.8.0/21',
        'ip4:130.211.16.0/20',
        'ip4:130.211.32.0/19',
        '?all'
    ),
    '_cloud-netblocks6.googleusercontent.com.': (
        'v=spf1',
        'ip4:130.211.64.0/18',
        'ip4:130.211.128.0/17',
        'ip4:146.148.2.0/23',
        'ip4:146.148.4.0/22',
        'ip4:146.148.8.0/21',
        'ip4:146.148.16.0/20',
        'ip4:146.148.32.0/19',
        'ip4:146.148.64.0/18',
        'ip4:162.216.148.0/22',
        'ip4:162.222.176.0/21',
        'ip4:173.255.112.0/20',
        'ip4:192.158.28.0/22',
        '?all',
    ),
    '_cloud-netblocks7.googleusercontent.com.': (
        'v=spf1',
        'ip4:199.192.112.0/22',
        'ip4:199.223.232.0/22',
        'ip4:199.223.236.0/23',
        'ip4:208.68.108.0/23',
        '?all',
    ),
    '_spf.google.com.': (
        'v=spf1',
        'include:_netblocks.google.com',
        'include:_netblocks2.google.com',
        'include:_netblocks3.google.com ~all'
    ),
    '_netblocks.google.com.': (
        'v=spf1',
        'ip4:35.190.247.0/24',
        'ip4:64.233.160.0/19',
        'ip4:66.102.0.0/20',
        'ip4:66.249.80.0/20',
        'ip4:72.14.192.0/18',
        'ip4:74.125.0.0/16',
        'ip4:108.177.8.0/21',
        'ip4:173.194.0.0/16',
        'ip4:209.85.128.0/17',
        'ip4:216.58.192.0/19',
        'ip4:216.239.32.0/19',
        '~all'
    ),
    '_netblocks2.google.com.': (
        'v=spf1',
        'ip6:2001:4860:4000::/36',
        'ip6:2404:6800:4000::/36',
        'ip6:2607:f8b0:4000::/36',
        'ip6:2800:3f0:4000::/36',
        'ip6:2a00:1450:4000::/36',
        'ip6:2c0f:fb50:4000::/36',
        '~all'
    ),
    '_netblocks3.google.com.': (
        'v=spf1',
        'ip4:172.217.0.0/19',
        'ip4:172.217.32.0/20',
        'ip4:172.217.128.0/19',
        'ip4:172.217.160.0/20',
        'ip4:172.217.192.0/19',
        'ip4:172.253.56.0/21',
        'ip4:172.253.112.0/20',
        'ip4:108.177.96.0/19',
        'ip4:35.191.0.0/16',
        'ip4:130.211.0.0/22',
        '~all'
    ),
}
