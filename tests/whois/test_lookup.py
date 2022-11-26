"""
Unit tests for netlookup.whois.lookup module
"""
import pytest

from netlookup.exceptions import WhoisQueryError
from netlookup.whois import WhoisAddressLookup
from netlookup.whois.constants import WhoisQueryType
from netlookup.whois.lookup import QueryLookupCache

from .constants import MOCK_WHOIS_QUERY_ADDRESS, MOCK_WHOIS_QUERY_DOMAIN


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


def test_whois_query_lookup_cache_base_class_properties(address_list_file):
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
    with pytest.raises(NotImplementedError):
        obj.resolve_address_list_file(address_list_file)
    with pytest.raises(WhoisQueryError):
        obj.write_cache()


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


def test_whois_address_lookup_cache_write(mock_whois_default_cache) -> None:
    """
    Test properties of a WhoisAddressLookup with empty query cache
    """
    assert not mock_whois_default_cache.exists()
    whois = WhoisAddressLookup()
    assert not whois.cache_file.exists()

    whois.write_cache()
    assert whois.cache_file.exists()

    whois.cache_file.unlink()

    whois.write_cache()
    assert whois.cache_file.exists()


# pylint: disable=unused-argument
def test_whois_address_lookup_domain_success(mock_whois_default_cache, mock_whois_domain_query):
    """
    Test successful lookup for address lookup with mocked command output
    """
    whois = WhoisAddressLookup()
    response = whois.query(MOCK_WHOIS_QUERY_DOMAIN)
    assert mock_whois_domain_query.call_count == 1
    assert response.__query__ == MOCK_WHOIS_QUERY_DOMAIN
    assert response.__query_type__ == WhoisQueryType.DOMAIN
    assert whois.query(MOCK_WHOIS_QUERY_DOMAIN) == response
    assert mock_whois_domain_query.call_count == 1


# pylint: disable=unused-argument
def test_whois_address_lookup_address_success(mock_whois_default_cache, mock_whois_address_query):
    """
    Test successful lookup for address lookup with mocked command output
    """
    whois = WhoisAddressLookup()
    response = whois.query(MOCK_WHOIS_QUERY_ADDRESS)
    assert mock_whois_address_query.call_count == 1
    assert response.__query__ == MOCK_WHOIS_QUERY_ADDRESS
    assert response.__query_type__ == WhoisQueryType.ADDRESS
    assert whois.query(MOCK_WHOIS_QUERY_ADDRESS) == response
    assert mock_whois_address_query.call_count == 1
