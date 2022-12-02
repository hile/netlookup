"""
Unit tests for netlookup.whois.groups module
"""
import pytest

from netlookup.exceptions import WhoisQueryError
from netlookup.whois.groups import InformationSectionGroup, InetNum, Nameservers, Route

from .constants import (
    MOCK_INETNUM_LINE,
    MOCK_INETNUM_GROUP_AS_DICT,
    MOCK_INVALID_INETNUM_RANGE_LINE,
    MOCK_INETNUM_LINE_LIST,
    MOCK_NAMESERVER_LINE,
    MOCK_NAMESERVER_ONLY_HOSTNAME_LINE,
    MOCK_INVALID_NAMESERVER_LINE,
    MOCK_ROUTE_LINE,
)


def test_whois_groups_empty_group_properties(empty_whois_response):
    """
    Test properties of empty InformationSectionGroup object
    """
    group = InformationSectionGroup(empty_whois_response, MOCK_INETNUM_LINE)
    assert group.section == 'inetnum'
    assert group.is_empty is True
    assert group.as_dict() == {'inetnum': {}}


def test_whois_groups_parse_inetnum_properties(empty_whois_response):
    """
    Test properties of empty InformationSectionGroup object
    """
    group = InformationSectionGroup(empty_whois_response, MOCK_INETNUM_LINE)
    group.parse_line(MOCK_INETNUM_LINE)
    assert group.section == 'inetnum'
    assert group.is_empty is False
    assert group.as_dict() == MOCK_INETNUM_GROUP_AS_DICT


# pylint: disable=unused-argument
def test_whois_groups_parse_invalid_network_range(empty_whois_query_cache, empty_whois_response):
    """
    Test parsing of an invalid network range line
    """
    group = InetNum(empty_whois_response, MOCK_INVALID_INETNUM_RANGE_LINE)
    with pytest.raises(WhoisQueryError):
        group.parse_line(MOCK_INVALID_INETNUM_RANGE_LINE)


def test_whois_groups_parse_inetnum_merge_networks_duplicate(empty_whois_response):
    """
    Test properties of empty InformationSectionGroup object, parsing duplicate networks
    """
    group = InetNum(empty_whois_response, MOCK_INETNUM_LINE)
    group.parse_line(MOCK_INETNUM_LINE)
    assert len(group.address_ranges) == 1
    assert len(group.networks) == 1
    group.parse_line(MOCK_INETNUM_LINE)
    assert len(group.address_ranges) == 1
    assert len(group.networks) == 1
    assert isinstance(group.as_dict(), dict)


def test_whois_groups_parse_inetnum_merge_list_of_networks_duplicate(empty_whois_response):
    """
    Test properties of empty InformationSectionGroup object, parsing duplicate networks
    """
    group = InetNum(empty_whois_response, MOCK_INETNUM_LINE)
    group.parse_line(MOCK_INETNUM_LINE)
    assert len(group.address_ranges) == 1
    assert len(group.networks) == 1
    group.parse_line(MOCK_INETNUM_LINE_LIST)
    assert len(group.address_ranges) == 3
    assert len(group.networks) == 3
    assert isinstance(group.as_dict(), dict)


def test_whois_groups_route_nameserver(empty_whois_response):
    """
    Test properties of empty Route object, parsing the mocked route line
    """
    group = Nameservers(empty_whois_response, MOCK_NAMESERVER_LINE)

    group.parse_line(MOCK_NAMESERVER_LINE)
    assert len(group.address_ranges) == 0
    assert len(group.networks) == 0

    group.parse_line(MOCK_NAMESERVER_ONLY_HOSTNAME_LINE)
    assert len(group.address_ranges) == 0
    assert len(group.networks) == 0

    group.parse_line(MOCK_INVALID_NAMESERVER_LINE)
    assert len(group.address_ranges) == 0
    assert len(group.networks) == 0

    assert isinstance(group.as_dict(), dict)


def test_whois_groups_route(empty_whois_response):
    """
    Test properties of empty Route object, parsing the mocked route line
    """
    group = Route(empty_whois_response, MOCK_ROUTE_LINE)
    group.parse_line(MOCK_ROUTE_LINE)
    assert len(group.address_ranges) == 0
    assert len(group.networks) == 1
    group.parse_line(MOCK_ROUTE_LINE)
    assert len(group.address_ranges) == 0
    assert len(group.networks) == 1
    assert isinstance(group.as_dict(), dict)
