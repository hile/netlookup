"""
Test whois query utilities
"""

from datetime import datetime

import pytest

from netaddr.ip import IPNetwork, IPRange

from systematic_networks.exceptions import WhoisQueryError
from systematic_networks.whois.constants import GLOBAL_FIELD_MAP
from systematic_networks.whois.lookup import WhoisAddressLookup
from systematic_networks.whois.response import WhoisQueryResponse
from systematic_networks.whois.utils import (
    lookup_field_alias,
    parse_datetime,
    parse_field_value,
    parse_network_value,
)


def test_whois_utils_parse_datetime():
    """
    Test whois utility to parse datetimes
    """
    values = (
        '2020-01-02T00:11:22Z',
        '2020-01-02T00:11:22+02:00',
        '2020-01-02',
        1.2345,
    )
    for value in values:
        assert isinstance(parse_datetime(value), datetime)

    invalid = (
        '2020',
        'not a date'
    )
    for value in invalid:
        with pytest.raises(WhoisQueryError):
            parse_datetime(value)


def test_whois_utils_lookup_field_alias():
    """
    Test whois utility to lookup a field alias
    """
    response = WhoisQueryResponse(WhoisAddressLookup())
    assert lookup_field_alias(response, 'testalias') == ('testalias', None)
    assert lookup_field_alias(response, 'billing_c') == (
        'billing_c',
        GLOBAL_FIELD_MAP['billing_c']
    )


def test_whois_utils_parse_field_value():
    """
    Test parsing a whois output line to field and value
    """
    testcases = (
        ('LABEL', ('label', '')),
        ('CamelLabel', ('camel_label', '')),
        ('foo: bar baz', ('foo', 'bar baz')),
        ('foo...: bar baz', ('foo', 'bar baz')),
    )
    for testcase in testcases:
        result = parse_field_value(testcase[0])
        assert result == testcase[1]

    assert parse_field_value('NOT A FIELD OR LABEL') == (None, None)


def test_whois_utils_parse_network_value():
    """
    Test parsing network values
    """
    range_testcases = (
        '192.168.0.1 - 192.168.0.2',
    )
    for testcase in range_testcases:
        ranges = parse_network_value(testcase)
        assert isinstance(ranges, list)
        for value in ranges:
            assert isinstance(value, IPRange)

    network_testcases = (
        ' fe80::/64',
        '192.168.0.024',
        '192.168.0.024, 192.168.1.024,  fe80::/64',
    )
    for testcase in network_testcases:
        networks = parse_network_value(testcase)
        assert isinstance(networks, list)
        for network in networks:
            assert isinstance(network, IPNetwork)

    invalid_values = (
        'not-a-net',
        '192 168.0.1 - test',
        '192.168.0.024, test',
    )
    for testcase in invalid_values:
        with pytest.raises(WhoisQueryError):
            parse_network_value(testcase)
