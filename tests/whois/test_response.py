"""
Unit tests for netlookup.whois.response module
"""
import pytest

from netlookup.exceptions import WhoisQueryError
from netlookup.whois import PrefixLookup, WhoisLookup
from netlookup.whois.constants import WhoisQueryType
from netlookup.whois.response import PrefixLookupResponse, WhoisLookupResponse

from .constants import (
    MOCK_WHOIS_QUERY_ADDRESS,
    MOCK_WHOIS_QUERY_DOMAIN,
    MOCK_PWHOIS_QUERY_ADDRESS,
    MOCK_PWHOIS_QUERY_MATCH,
)


def test_whois_response_properties():
    """
    Test properties of a plain WhoisLookupResponse object with no query
    """
    response = WhoisLookupResponse(whois=WhoisLookup())
    assert response.__query_type__ is None
    assert response.__detect_query_type__('foo.bar') == WhoisQueryType.DOMAIN.value
    with pytest.raises(WhoisQueryError):
        response.__detect_query_type__('')

    assert isinstance(response.__repr__(), str)
    assert response.__repr__() == """<class 'netlookup.whois.response.WhoisLookupResponse'>"""
    assert isinstance(response.description, str)
    assert response.description == ''
    assert response.match(MOCK_WHOIS_QUERY_ADDRESS) is False


# pylint: disable=unused-argument
def test_whois_response_address_properties(mock_whois_default_cache, mock_whois_domain_query):
    """
    Test successful lookup for address lookup with mocked command output
    """
    response = WhoisLookup()(MOCK_WHOIS_QUERY_ADDRESS)
    assert isinstance(response.__repr__(), str)
    assert isinstance(response.description, str)
    assert isinstance(response.as_json(), str)
    assert isinstance(response.as_dict(), dict)


# pylint: disable=unused-argument
def test_whois_response_address_match_found(mock_whois_default_cache, mock_whois_domain_query):
    """
    Test matching response to original response field with address, match is found
    """
    response = WhoisLookup()(MOCK_WHOIS_QUERY_ADDRESS)
    assert response.match(MOCK_WHOIS_QUERY_ADDRESS) is True


# pylint: disable=unused-argument
def test_whois_response_address_match__not_found(
        mock_whois_default_cache, mock_whois_domain_query):
    """
    Test matching response to original response field with different address, match is  not found
    """
    response = WhoisLookup()(MOCK_WHOIS_QUERY_ADDRESS)
    assert response.match(MOCK_PWHOIS_QUERY_ADDRESS) is False


# pylint: disable=unused-argument
def test_whois_response_domain_properties(mock_whois_default_cache, mock_whois_domain_query):
    """
    Test successful lookup for address lookup with mocked command output
    """
    response = WhoisLookup()(MOCK_WHOIS_QUERY_DOMAIN)
    assert isinstance(response.__repr__(), str)
    assert isinstance(response.description, str)
    assert isinstance(response.as_json(), str)
    assert isinstance(response.as_dict(), dict)


# pylint: disable=unused-argument
def test_whois_response_domain_match_found(mock_whois_default_cache, mock_whois_domain_query):
    """
    Test matching response to original response field with domain, match is found
    """
    response = WhoisLookup()(MOCK_WHOIS_QUERY_DOMAIN)
    assert response.match(MOCK_WHOIS_QUERY_DOMAIN) is True


# pylint: disable=unused-argument
def test_whois_response_domain_match_address_not_found(
        mock_whois_default_cache, mock_whois_domain_query):
    """
    Test matching response to address field with domain, no match is found
    """
    response = WhoisLookup()(MOCK_WHOIS_QUERY_DOMAIN)
    assert response.match(MOCK_WHOIS_QUERY_ADDRESS) is False


def test_whois_prefix_lookup_response_empty_response_properties():
    """
    Test properties of an empty PrefixLookupResponse objet
    """
    obj = PrefixLookupResponse(PrefixLookup())
    assert isinstance(obj.__repr__(), str)
    assert obj.__repr__() == ''

    assert obj.match(MOCK_PWHOIS_QUERY_ADDRESS) is False

    assert isinstance(obj.as_dict(), dict)
    assert isinstance(obj.as_json(), str)

    obj.__query__ = MOCK_PWHOIS_QUERY_ADDRESS
    assert obj.match(MOCK_PWHOIS_QUERY_ADDRESS) is True


# pylint: disable=unused-argument
def test_whois_prefix_lookup_response_valid_response_properties(
        mock_whois_query_no_data,
        mock_whois_lookup_cache,
        mock_prefix_lookup_cache):
    """
    Test properties of an valid PrefixLookupResponse objet
    """
    obj = mock_prefix_lookup_cache.match(MOCK_PWHOIS_QUERY_MATCH)
    assert isinstance(obj.__repr__(), str)

    assert obj.match(MOCK_PWHOIS_QUERY_MATCH) is True
    assert isinstance(obj.as_dict(), dict)
    assert isinstance(obj.as_json(), str)
