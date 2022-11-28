"""
Unit test constants for netlookup.whois modul
"""

MOCK_INETNUM_LINE = 'inetnum: 1.2.3.0 - 1.2.3.255'

MOCK_WHOIS_QUERY_DOMAIN = 'tuohela.net'
MOCK_WHOIS_QUERY_ADDRESS = '1.2.3.4'
MOCK_PWHOIS_QUERY_ADDRESS = '192.168.23.4'

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
