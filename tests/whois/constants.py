"""
Unit test constants for netlookup.whois modul
"""
from netaddr.ip import IPNetwork, IPRange

MOCK_INETNUM_LINE = 'inetnum: 1.2.3.0 - 1.2.3.255'
MOCK_INVALID_INETNUM_RANGE_LINE = 'inetnum: 10.0.0.0 - 1.2.3.255'
MOCK_INETNUM_LINE_LIST = 'inetnum: 1.2.6.0 - 1.2.6.255,1.2.8.0 - 1.2.8.31'
MOCK_ROUTE_LINE = 'route: 103.102.250.0/24'

MOCK_NAMESERVER_LINE = 'nserver: A.GTLD-SERVERS.NET 192.5.6.30 2001:503:a83e:0:0:0:2:30'
MOCK_NAMESERVER_ONLY_HOSTNAME_LINE = 'nserver: C.GTLD-SERVERS.NET'
MOCK_INVALID_NAMESERVER_LINE = 'nserver: B.GTLD-SERVERS.NET 1.2.3'

# Yes this is a bit nonsense as shown here :)
MOCK_INETNUM_GROUP_AS_DICT = {
    'inetnum': {
        'inetnum': {
            'value': IPRange('1.2.3.0', '1.2.3.255'),
            'description': 'Inetnum'
        }
    }
}

MOCK_INVALID_NETWORK_LINE = '192.168.256.0/24'

MOCK_WHOIS_QUERY_DOMAIN = 'tuohela.net'
MOCK_WHOIS_QUERY_ADDRESS = '103.102.250.5'

MOCK_PWHOIS_QUERY_MATCH = '2001:708:10:dead:beef::1'
MOCK_PWHOIS_QUERY_ADDRESS = '192.168.23.1'

MOCK_PWHOIS_QUERY_MATCH_NETWORKS = [
    IPNetwork('2001:708:10::/48'),
    IPNetwork('2001:600::/23'),
]
MOCK_PWHOIS_QUERY_RESPONSE_AS_JSON = """{
  "networks": [
    "2001:708:10::/48",
    "2001:600::/23"
  ]
}"""

MOCK_PWHOIS_RESPONSE_COUNT = 4

INVALID_DATETIME_VALUES = (
    None,
    '',
    '2021-02-29',
)

VALID_DATETIME_VALUES = (
    '2022-01-20',
    '2022-01-20T12:23:34Z',
    123456789,
    123456789.1234,
)

INVALID_FIELD_VALUES = (
    '',
    'this is not a valid field',
    'field:value missing prefix space',
)

VALID_FIELD_VALUES = (
    'field1_underscores: other value',
    'demolabel',
)

INVALID_WHOIS_RESPONSE_NETWORK_VALUES = (
    '1.2.3.4 - 1.2.3.',
    '1.2.3.4-1.2.3.8',
    '1.2.3.4-1.2.3',
    '1.2.3.4-',
)


VALID_WHOIS_RESPONSE_IPRANGE_VALUES = (
    '1.2.3.4 - 1.2.3.8',
)


VALID_WHOIS_RESPONSE_NETWORK_VALUES = (
    '10.0.0.0/8',
    '192.168.1.0/24,192.168.2.0/24',
)
