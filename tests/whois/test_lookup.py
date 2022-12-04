"""
Unit tests for netlookup.whois.lookup module
"""
import pytest

from netaddr.ip import IPAddress

from netlookup.exceptions import WhoisQueryError
from netlookup.whois import PrefixLookup, WhoisLookup
from netlookup.whois.constants import WhoisQueryType, RESPONSE_MAX_AGE_SECONDS
from netlookup.whois.lookup import QueryLookupCache, PREFIX_CACHE_FILE, WHOIS_CACHE_FILE
from netlookup.whois.response import PrefixLookupResponse, WhoisLookupResponse

from ..conftest import MOCK_WHOIS_CACHE_RESPONSE_COUNT
from .constants import (
    MOCK_PWHOIS_RESPONSE_COUNT,
    MOCK_PWHOIS_QUERY_ADDRESS,
    MOCK_PWHOIS_QUERY_MATCH,
    MOCK_WHOIS_QUERY_ADDRESS,
    MOCK_WHOIS_QUERY_DOMAIN,
    MOCK_WHOIS_QUERY_MATCH_NETWORKS,
)
from .conftest import MOCK_DOMAIN_KEY_MATCH_COUNT, MOCK_INETNUM_KEY_MATCH_COUNT


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
def test_whois_domain_lookup_cache_file(
        mock_whois_query_no_data,
        mock_whois_lookup_cache):
    """
    Mock loading whois lookup object with cached items
    """
    whois = mock_whois_lookup_cache
    assert whois.__default_cache_file__ == WHOIS_CACHE_FILE
    assert whois.cache_file.exists()
    assert isinstance(whois, WhoisLookup)
    response = whois.query(MOCK_WHOIS_QUERY_DOMAIN)
    assert isinstance(response, WhoisLookupResponse)
    assert isinstance(response.description, str)


def test_whois_domain_lookup_expired_cache_file(
        mock_whois_domain_query,
        mock_whois_lookup_cache_expired):
    """
    Mock whois cache lookup for address when all cache items are expired
    """
    whois = mock_whois_lookup_cache_expired
    # Item is not valid (expired)
    assert whois.match(MOCK_WHOIS_QUERY_DOMAIN, max_age=30) is None
    # Known address but the response is marked as expired, must query again
    response = whois.query(MOCK_WHOIS_QUERY_DOMAIN)
    assert isinstance(response, WhoisLookupResponse)
    assert mock_whois_domain_query.call_count == 1


def test_whois_domain_lookup_unloaded_cache_file(
        mock_whois_domain_query,
        mock_whois_lookup_cache_unloaded):
    """
    Mock whois cache lookup for address when all cache items are unloaded (load timestamp is
    none)
    """
    whois = mock_whois_lookup_cache_unloaded
    # Item is not valid (unloaded)
    assert whois.match(MOCK_WHOIS_QUERY_DOMAIN, max_age=30) is None
    # Known address but the response is marked as expired, must query again
    response = whois.query(MOCK_WHOIS_QUERY_DOMAIN)
    assert isinstance(response, WhoisLookupResponse)
    assert mock_whois_domain_query.call_count == 1

    assert isinstance(response.description, str)


def test_whois_address_lookup_unloaded_cache_file(
        mock_whois_address_query,
        mock_whois_lookup_cache_unloaded):
    """
    Mock whois cache lookup for address when all cache items are unloaded
    """
    whois = mock_whois_lookup_cache_unloaded
    # Known address but the response is marked as expired, must query again
    response = whois.query(MOCK_WHOIS_QUERY_ADDRESS)
    assert isinstance(response, WhoisLookupResponse)
    assert mock_whois_address_query.call_count == 1
    assert response.networks == MOCK_WHOIS_QUERY_MATCH_NETWORKS
    assert isinstance(response.description, str)


def test_whois_address_lookup_expired_cache_file(
        mock_whois_address_query,
        mock_whois_lookup_cache_expired):
    """
    Mock whois cache lookup for address when all cache items are expired
    """
    whois = mock_whois_lookup_cache_expired
    # Known address but the response is marked as expired, must query again
    response = whois.query(MOCK_WHOIS_QUERY_ADDRESS)
    assert isinstance(response, WhoisLookupResponse)
    assert mock_whois_address_query.call_count == 1


# pylint: disable=unused-argument
def test_whois_address_lookup_query_error(
        mock_whois_command_error,
        empty_whois_query_cache):
    """
    Test whois query when command line raises an error
    """
    with pytest.raises(WhoisQueryError):
        empty_whois_query_cache.query(MOCK_WHOIS_QUERY_ADDRESS)


# pylint: disable=unused-argument
def test_whois_prefix_lookup_cache_file(
        mock_whois_query_no_data,
        mock_whois_lookup_cache,
        mock_prefix_lookup_cache):
    """
    Mock loading prefix lookup object with cached items
    """
    prefixes = mock_prefix_lookup_cache
    assert prefixes.__default_cache_file__ == PREFIX_CACHE_FILE
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

    assert whois.query(MOCK_WHOIS_QUERY_ADDRESS) == response
    assert mock_whois_address_query.call_count == 1


# pylint: disable=unused-argument
def test_whois_domain_lookup_filter_keys(mock_whois_lookup_cache):
    """
    Test filtering of items by group key from whois query cache
    """
    matches = mock_whois_lookup_cache.filter_keys('domain')
    print(len(matches), len(mock_whois_lookup_cache.__responses__))
    assert len(matches) == MOCK_DOMAIN_KEY_MATCH_COUNT


# pylint: disable=unused-argument
def test_whois_address_lookup_filter_keys(mock_whois_lookup_cache):
    """
    Test filtering of items by group key from whois query cache
    """
    matches = mock_whois_lookup_cache.filter_keys('inetnum')
    print(len(matches), len(mock_whois_lookup_cache.__responses__))
    assert len(matches) == MOCK_INETNUM_KEY_MATCH_COUNT


def test_whois_prefix_lookup_query_empty_cache(
        empty_prefix_lookup_query_cache,
        mock_prefix_lookup_query):
    """
    Test query() method of prefix lookup when a match is found
    """
    assert len(empty_prefix_lookup_query_cache.__responses__) == 0
    assert empty_prefix_lookup_query_cache.match(MOCK_PWHOIS_QUERY_MATCH) is None

    response = empty_prefix_lookup_query_cache.query(MOCK_PWHOIS_QUERY_MATCH)
    assert isinstance(response, PrefixLookupResponse)


# pylint: disable=unused-argument
def test_whois_prefix_lookup_query_query_error(
        mock_whois_command_error,
        empty_prefix_lookup_query_cache):
    """
    Test prefix lookup query when command line raises an error
    """
    with pytest.raises(WhoisQueryError):
        empty_prefix_lookup_query_cache.query(MOCK_PWHOIS_QUERY_MATCH)


def test_whois_prefix_lookup_query_cache_write_readonly_error(
        capsys,
        mock_prefix_lookup_default_cache_readonly,
        mock_prefix_lookup_query) -> None:
    """
    Test writing whois lookup cache file when cache file is readonly and write failss
    """
    assert not mock_prefix_lookup_default_cache_readonly.exists()
    prefix_lookup = PrefixLookup()
    with pytest.raises(WhoisQueryError):
        prefix_lookup.write_cache()

    # Query writes error message to stderr when cache can't be written but does not fail
    prefix_lookup.__debug_enabled__ = True
    response = prefix_lookup.query(MOCK_PWHOIS_QUERY_MATCH)
    assert isinstance(response, PrefixLookupResponse)
    captured = capsys.readouterr()
    debug = captured.err.splitlines()
    # Also contains debug prints from query
    assert len(debug) > 1
    prefix = f'error updating cache file {prefix_lookup.cache_file}'
    assert debug[-1][:len(prefix)] == prefix


def test_whois_prefix_lookup_match_found(mock_prefix_lookup_cache):
    """
    Test match() method of prefix lookup when a match is found
    """
    response = mock_prefix_lookup_cache.match(MOCK_PWHOIS_QUERY_MATCH)
    assert isinstance(response, PrefixLookupResponse)


def test_whois_prefix_lookup_match_expired(mock_prefix_lookup_cache_expired):
    """
    Test match() method of prefix lookup when a match is found
    """
    response = mock_prefix_lookup_cache_expired.match(
        MOCK_PWHOIS_QUERY_MATCH,
        max_age=RESPONSE_MAX_AGE_SECONDS
    )
    assert response is None

    # Default max_age is None for match() method
    response = mock_prefix_lookup_cache_expired.match(MOCK_PWHOIS_QUERY_MATCH)
    assert isinstance(response, PrefixLookupResponse)


def test_whois_prefix_lookup_query_expired_no_data(mock_prefix_lookup_cache_expired, mock_whois_query_no_data):
    """
    Test query() method of prefix lookup when cache is expired and no data is received from server
    """
    with pytest.raises(WhoisQueryError):
        mock_prefix_lookup_cache_expired.query(MOCK_PWHOIS_QUERY_MATCH)
