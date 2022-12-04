"""
Unit tests for netlookup.whois.utils module
"""
from datetime import datetime

import pytest
from netaddr.ip import IPAddress, IPNetwork, IPRange

from netlookup.constants import IPV4_VERSION, IPV6_VERSION, MAX_PREFIX_LEN_IPV4, MAX_PREFIX_LEN_IPV6
from netlookup.exceptions import WhoisQueryError
from netlookup.whois.utils import parse_datetime, parse_field_value, parse_network_value


def test_whois_utils_parse_datetime_invalid_values(invalid_datetime_value) -> None:
    """
    Test parse_datetime method with various invalid datetime values
    """
    with pytest.raises(WhoisQueryError):
        parse_datetime(invalid_datetime_value)


def test_whois_utils_parse_datetime_valid_values(valid_datetime_value) -> None:
    """
    Test parse_datetime method with various valid datetime values
    """
    value = parse_datetime(valid_datetime_value)
    assert isinstance(value, datetime)


def test_whois_utils_parse_field_value_invalid_value(invalid_field_value) -> None:
    """
    Test parse_field_value with invalid values
    """
    assert parse_field_value(invalid_field_value) == (None, None)


def test_whois_utils_parse_field_value_valid_value(valid_field_value) -> None:
    """
    Test parse_field_value with invalid values
    """
    field, value = parse_field_value(valid_field_value)
    assert isinstance(field, str)
    assert field != ''
    assert isinstance(value, str)
    if valid_field_value.count(' ') > 0:
        assert value != ''
    else:
        assert value == ''


def test_whois_utils_parse_network_value_invalid_values(invalid_whois_network_value):
    """
    Test parse_network_value with invalid values
    """
    with pytest.raises(WhoisQueryError):
        parse_network_value(invalid_whois_network_value)


def test_whois_utils_parse_network_value_valid_iprange_values(valid_whois_iprange_value):
    """
    Test parse_network_value with valid values as IP network objects
    """
    result = parse_network_value(valid_whois_iprange_value)
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, IPRange)


def test_whois_utils_parse_network_value_valid_network_values(valid_whois_networks_value):
    """
    Test parse_network_value with valid values as IP network objects
    """
    result = parse_network_value(valid_whois_networks_value)
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, (IPAddress, IPNetwork))
