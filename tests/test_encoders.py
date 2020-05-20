"""
Test JSON encoders
"""

import json

from datetime import datetime

from netaddr.ip import IPAddress, IPNetwork, IPRange

from systematic_networks.encoders import NetworkDataEncoder


def validate_network_json_dump(testdata):
    """
    Validate network data encodes to strings
    """
    output = json.dumps(testdata, cls=NetworkDataEncoder)
    assert isinstance(output, str)
    parsed = json.loads(output)
    assert 'ipv4' in parsed
    assert isinstance(parsed['ipv4'], str)
    assert 'ipv6' in parsed
    assert isinstance(parsed['ipv6'], str)


def test_encoders_network_data_ip_addresses():
    """
    Test encoding IPv4 and IPv6 addresses
    """
    testdata = {
        'strings': 'strings and violins',
        'datetime': datetime.now(),
        'ipv4': IPAddress('127.0.0.1'),
        'ipv6': IPAddress('fe80::cf5:7a26:8467:1de1')
    }
    validate_network_json_dump(testdata)


def test_encoders_network_data_ip_networks():
    """
    Test encoding IPv4 and IPv6 addresses
    """
    testdata = {
        'strings': 'strings and violins',
        'datetime': datetime.now(),
        'ipv4': IPNetwork('192.168.1.0/24'),
        'ipv6': IPNetwork('fe80::cf5:7a26/64')
    }
    validate_network_json_dump(testdata)


def test_encoders_network_data_ip_ranges():
    """
    Test encoding IPv4 and IPv6 addresses
    """
    testdata = {
        'strings': 'strings and violins',
        'datetime': datetime.now(),
        'ipv4': IPRange('192.168.1.1', '192.168.1.2'),
        'ipv6': IPRange('fe80::cf5:7a26:8467:1de1', 'fe80::cf5:7a26:8467:1df1')
    }
    validate_network_json_dump(testdata)
