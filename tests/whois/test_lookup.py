"""
Unit tests for netlookup.whois.lookup module
"""
import pytest

from netaddr.ip import IPAddress

from netlookup.exceptions import WhoisQueryError
from netlookup.whois import PrefixLookup, WhoisLookup
from netlookup.whois.constants import WhoisQueryType
from netlookup.whois.lookup import QueryLookupCache, PREFIX_CACHE_FILE, WHOIS_CACHE_FILE
from netlookup.whois.response import PrefixLookupResponse, WhoisLookupResponse

from ..conftest import MOCK_WHOIS_CACHE_RESPONSE_COUNT
from .constants import (
    MOCK_PWHOIS_RESPONSE_COUNT,
    MOCK_PWHOIS_QUERY_ADDRESS,
    MOCK_WHOIS_QUERY_ADDRESS,
    MOCK_WHOIS_QUERY_DOMAIN,
)


def validate_empty_address_lookup_cache(whois: WhoisLookup) -> None:
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

    assert whois.match(MOCK_WHOIS_QUERY_ADDRESS) is None
    assert whois.match(IPAddress(MOCK_WHOIS_QUERY_ADDRESS)) is None

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
        obj.resolve_lookup_strings(address_list_file)
    with pytest.raises(WhoisQueryError):
        obj.write_cache()


# pylint: disable=unused-argument
def test_whois_address_lookup_resolve_lookup_strings(
        mock_whois_lookup_cache,
        mock_whois_address_query,
        address_list_file):
    """
    Test whois address lookup function to resolve a list of addresses
    """
    whois = mock_whois_lookup_cache
    assert len(whois.__responses__) == MOCK_WHOIS_CACHE_RESPONSE_COUNT
    whois.resolve_lookup_strings(address_list_file)
    # Two items in cache were not part of the mocked cache and were mock resolved
    assert len(whois.__responses__) == MOCK_WHOIS_CACHE_RESPONSE_COUNT + 2


# pylint: disable=unused-argument
def test_whois_address_lookup_resolve_lookup_strings_query_error(
        capsys,
        mock_whois_lookup_cache,
        mock_whois_query_no_data,
        address_list_file):
    """
    Test whois address lookup function to resolve a list of addresses with query errors
    """
    whois = mock_whois_lookup_cache
    assert len(whois.__responses__) == MOCK_WHOIS_CACHE_RESPONSE_COUNT
    whois.resolve_lookup_strings(address_list_file)
    # Two non-matches resulted to query errors
    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 2
    assert len(whois.__responses__) == MOCK_WHOIS_CACHE_RESPONSE_COUNT


def test_whois_address_lookup_empty_default_cache_properties(mock_whois_default_cache):
    """
    Test properties of a WhoisLookup with empty default query cache
    """
    whois = WhoisLookup()
    assert whois.cache_file == mock_whois_default_cache
    validate_empty_address_lookup_cache(whois)


def test_whois_address_lookup_empty_cache_properties(empty_whois_query_cache) -> None:
    """
    Test properties of a WhoisLookup with empty query cache
    """
    validate_empty_address_lookup_cache(empty_whois_query_cache)


# pylint: disable=unused-argument
def test_whois_address_lookup_cache_file(
        mock_whois_query_no_data,
        mock_whois_lookup_cache):
    """
    Mock loading whois lookup object with cached items
    """
    whois = mock_whois_lookup_cache
    assert whois.__default_cache_file__ == WHOIS_CACHE_FILE
    assert whois.cache_file.exists()
    assert isinstance(whois, WhoisLookup)
    for item in whois.__dns_lookup_table__.values():
        print(item)
    res = whois.query(MOCK_WHOIS_QUERY_DOMAIN)
    assert isinstance(res, WhoisLookupResponse)


# pylint: disable=unused-argument
def test_prefix_address_lookup_cache_file(
        mock_whois_query_no_data,
        mock_whois_lookup_cache,
        mock_prefix_lookup_cache):
    """
    Mock loading prefix lookup object with cached items
    """
    prefixes = mock_prefix_lookup_cache
    assert prefixes.__default_cache_file__ == PREFIX_CACHE_FILE
    for prefix in prefixes.__responses__:
        print(prefix)
    assert len(prefixes.__responses__) == MOCK_PWHOIS_RESPONSE_COUNT
    assert prefixes.cache_file.exists()
    assert isinstance(prefixes, PrefixLookup)
    assert isinstance(prefixes.query(MOCK_PWHOIS_QUERY_ADDRESS), PrefixLookupResponse)
    # This returns the item with prefixes.match
    assert isinstance(prefixes.query(MOCK_PWHOIS_QUERY_ADDRESS), PrefixLookupResponse)
    assert isinstance(prefixes.match(MOCK_PWHOIS_QUERY_ADDRESS), PrefixLookupResponse)


def test_whois_address_lookup_cache_write(mock_whois_default_cache) -> None:
    """
    Test writing whois lookup cache file
    """
    assert not mock_whois_default_cache.exists()
    whois = WhoisLookup()
    assert not whois.cache_file.exists()

    whois.write_cache()
    assert whois.cache_file.exists()

    whois.cache_file.unlink()

    whois.write_cache()
    assert whois.cache_file.exists()


def test_whois_address_lookup_cache_write_readonly_error(
        capsys,
        mock_whois_default_cache_readonly,
        mock_whois_domain_query) -> None:
    """
    Test writing whois lookup cache file when cache file is readonly and write failss
    """
    assert not mock_whois_default_cache_readonly.exists()
    whois = WhoisLookup()
    with pytest.raises(WhoisQueryError):
        whois.write_cache()

    # Query writes error message to stderr when cache can't be written but does not fail
    whois.__debug_enabled__ = True
    response = whois.query(MOCK_WHOIS_QUERY_ADDRESS)
    assert isinstance(response, WhoisLookupResponse)
    captured = capsys.readouterr()
    debug = captured.err.splitlines()
    # Also contains debug prints from query
    assert len(debug) > 1
    prefix = f'error updating cache file {whois.cache_file}'
    assert debug[-1][:len(prefix)] == prefix


# pylint: disable=unused-argument
def test_whois_address_lookup_domain_success(mock_whois_default_cache, mock_whois_domain_query):
    """
    Test successful lookup for address lookup with mocked command output
    """
    whois = WhoisLookup()
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
    whois = WhoisLookup()
    response = whois.query(MOCK_WHOIS_QUERY_ADDRESS)
    assert mock_whois_address_query.call_count == 1
    assert response.__query__ == MOCK_WHOIS_QUERY_ADDRESS
    assert response.__query_type__ == WhoisQueryType.ADDRESS
    print(response)
    assert whois.query(MOCK_WHOIS_QUERY_ADDRESS) == response
    assert mock_whois_address_query.call_count == 1
