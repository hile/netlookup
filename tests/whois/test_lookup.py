"""
Unit tests for netlookup.whois.lookup module
"""
import pytest

from netlookup.whois.lookup import QueryLookupCache, WhoisAddressLookup


def validate_empty_address_lookup_cache(whois: WhoisAddressLookup) -> None:
    """
    Validate properties of an empty whois address lookup cache
    """
    assert callable(whois)

    assert whois.__debug_enabled__ is False
    assert whois.__silent__ is False

    assert len(whois.__responses__) == 0

    # pylint: disable=use-implicit-booleaness-not-comparison
    assert whois.__dns_lookup_table__ == {}

    # pylint: disable=use-implicit-booleaness-not-comparison
    assert whois.__unmapped_fields__ == {}

    assert whois.match('1.2.3.4') is None

    # pylint: disable=use-implicit-booleaness-not-comparison
    assert whois.filter_keys('test_key') == []


def test_whois_query_lookup_cache_base_class_properties():
    """
    Test properties of a QueryLookupCache base class object
    """
    obj = QueryLookupCache()
    assert callable(obj)
    assert obj.__default_cache_file__ is None
    with pytest.raises(NotImplementedError):
        obj('lookup-this')
    with pytest.raises(NotImplementedError):
        obj.match('no such thing')


def test_whois_address_lookup_empty_default_cache_properties(mock_whois_default_cache):
    """
    Test properties of a WhoisAddressLookup with empty default query cache
    """
    whois = WhoisAddressLookup()
    assert whois.cache_file == mock_whois_default_cache
    validate_empty_address_lookup_cache(whois)


def test_whois_address_lookup_empty_cache_properties(empty_whois_query_cache) -> None:
    """
    Test properties of a WhoisAddressLookup with empty query cache
    """
    validate_empty_address_lookup_cache(empty_whois_query_cache)
