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
  "inet6num": [
    {
      "inet6num": {
        "value": "2001:600::/23",
        "description": "Inet6num"
      },
      "organization": {
        "value": "RIPE NCC",
        "description": "Organization"
      },
      "status": {
        "value": "ALLOCATED",
        "description": "Status"
      }
    },
    {
      "inet6num": {
        "value": "2001:708:10::/48",
        "description": "Inet6num"
      },
      "network_name": {
        "value": "CSC-IPV6-NET",
        "description": "Network Name"
      },
      "descr": {
        "value": "CSC - IT Center for Science Ltd",
        "description": "Description"
      },
      "country": {
        "value": "FI",
        "description": "Country Code"
      },
      "admin_c": {
        "value": "FH437-RIPE",
        "description": "Admin Contact"
      },
      "tech_c": {
        "value": "FH437-RIPE",
        "description": "Technical Contact"
      },
      "status": {
        "value": "ASSIGNED",
        "description": "Status"
      },
      "mnt_by": {
        "value": "AS1741-MNT",
        "description": "Maintainer"
      },
      "created": {
        "value": "2011-10-28T07:48:18+00:00",
        "description": "Created"
      },
      "last_modified": {
        "value": "2011-10-28T07:48:18+00:00",
        "description": "Last Modified"
      },
      "source": {
        "value": "RIPE",
        "description": "Source"
      }
    }
  ],
  "whois": {
    "whois": {
      "value": "whois.ripe.net",
      "description": "Whois"
    }
  },
  "changed": {
    "changed": {
      "value": "1999-06-30T21:00:00+00:00",
      "description": "Changed"
    },
    "source": {
      "value": "IANA",
      "description": "Source"
    }
  },
  "role": {
    "role": {
      "value": "FUNET Hostmaster",
      "description": "Role"
    },
    "address": {
      "value": [
        "CSC - IT Center for Science",
        "PO Box 405, FIN-02101 Espoo",
        "Finland"
      ],
      "description": "Postal Address"
    },
    "organization": {
      "value": "ORG-FF1-RIPE",
      "description": "Organization"
    },
    "phone": {
      "value": "+358 9 457 2704",
      "description": "Phone Number"
    },
    "admin_c": {
      "value": "TK5724-RIPE",
      "description": "Admin Contact"
    },
    "tech_c": {
      "value": [
        "KH622-RIPE",
        "AR414-RIPE",
        "JS12328-RIPE"
      ],
      "description": "Technical Contact"
    },
    "nic_hdl": {
      "value": "FH437-RIPE",
      "description": "NIC Handle"
    },
    "mnt_by": {
      "value": "AS1741-MNT",
      "description": "Maintainer"
    },
    "abuse_mailbox": {
      "value": "abuse@funet.fi",
      "description": "Abuse Mailbox"
    },
    "created": {
      "value": "2002-06-13T07:20:35+00:00",
      "description": "Created"
    },
    "last_modified": {
      "value": "2022-08-22T17:17:33+00:00",
      "description": "Last Modified"
    },
    "source": {
      "value": "RIPE # Filtered",
      "description": "Source"
    }
  },
  "route6": {
    "route6": {
      "value": "2001:708:10::/48",
      "description": "Route6"
    },
    "descr": {
      "value": "FUNET 2001:708:10::/48",
      "description": "Description"
    },
    "origin_as": {
      "value": "AS1741",
      "description": "Origin AS"
    },
    "mnt_by": {
      "value": "AS1741-MNT",
      "description": "Maintainer"
    },
    "created": {
      "value": "2013-11-04T10:41:34+00:00",
      "description": "Created"
    },
    "last_modified": {
      "value": "2013-11-04T10:41:34+00:00",
      "description": "Last Modified"
    },
    "source": {
      "value": "RIPE # Filtered",
      "description": "Source"
    }
  }
}"""
