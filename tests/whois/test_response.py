"""
Unit tests for netlookup.whois.response module
"""

from netlookup.whois import WhoisLookup

from .constants import MOCK_WHOIS_QUERY_ADDRESS, MOCK_WHOIS_QUERY_DOMAIN


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
def test_whois_response_domain_properties(mock_whois_default_cache, mock_whois_domain_query):
    """
    Test successful lookup for address lookup with mocked command output
    """
    response = WhoisLookup()(MOCK_WHOIS_QUERY_DOMAIN)
    assert isinstance(response.__repr__(), str)
    assert isinstance(response.description, str)
    assert isinstance(response.as_json(), str)
    assert isinstance(response.as_dict(), dict)
