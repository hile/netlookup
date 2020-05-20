"""
Unit tests for systematic_networks.whois.lookup module
"""

from systematic_networks.whois.lookup import WhoisAddressLookup


def test_whois_lookup_properties():
    """
    Test properties of whois lookup base class with mocked cache path

    Cache is empty and no data is included
    """
    whois = WhoisAddressLookup()
    assert whois.__debug_enabled__ is False
    assert whois.__silent__ is False
    assert len(whois.__responses__) == 0
    assert whois.__dns_lookup_table__ == {}
    assert whois.__unmapped_fields__ == {}

    assert whois.match('1.2.3.4') is None
    assert whois.filter_keys('test_key') == []
