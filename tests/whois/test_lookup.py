"""
Unit tests for netlookup.whois.lookup module
"""

from netlookup.whois.lookup import WhoisAddressLookup
from .mock import TEST_CACHE, TEST_CACHE_SIZE


def test_whois_lookup_properties():
    """
    Test properties of whois lookup base class with mocked cache path

    Cache is empty and no data is included
    """
    whois = WhoisAddressLookup()
    assert callable(whois)
    assert whois.__debug_enabled__ is False
    assert whois.__silent__ is False
    assert len(whois.__responses__) == 0
    assert whois.__dns_lookup_table__ == {}
    assert whois.__unmapped_fields__ == {}

    assert whois.match('1.2.3.4') is None
    assert whois.filter_keys('test_key') == []


def test_whois_cache_load(monkeypatch):
    """
    Test loading cache from test data file
    """
    monkeypatch.setattr(
        'netlookup.whois.lookup.DEFAULT_CACHE_FILE',
        TEST_CACHE
    )
    whois = WhoisAddressLookup()
    assert len(whois.__responses__) == TEST_CACHE_SIZE
    response = whois.match('0.0.0.0')
    assert response is None
    assert isinstance(whois.filter_keys('inetnum'), list)
