"""
Unit tests for netlookup.whois.response module
"""

from netaddr.ip import IPNetwork

from .mock import get_empty_response, get_test_reverse_lines, get_test_domain_lines

TEST_IPV4_ADDRESS = '1.2.3.4'
TEST_DOMAIN = 'example.com'


def test_whois_response_properties():
    """
    Test properties of empty WhoisQueryResponse object
    """
    response = get_empty_response()
    assert isinstance(response.__repr__(), str)
    none_attrs = (
        '__query_type__',
        '__query__',
        '__stdout__',
        '__stderr__',
        '__loaded__',
        'smallest_network',
    )
    for attr in none_attrs:
        assert getattr(response, attr) is None

    assert response.to_dict() == {'groups': []}
    assert response.as_json() == '{}'

    assert response.__detect_query_type__(TEST_IPV4_ADDRESS) == 'address'
    assert response.__detect_query_type__(TEST_DOMAIN) == 'domain'
    assert response.match(TEST_IPV4_ADDRESS) is None
    assert response.match(TEST_DOMAIN) is None

    response.__detect_networks__()
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert response.networks == []
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert response.address_ranges == []


def test_whois_response_mock_reverse():
    """
    Test loading WhoisQueryResponse from reverse record data
    """
    response = get_empty_response()
    response.__load_data__(get_test_reverse_lines(), [])
    assert response.__query_type__ == 'address'
    network = IPNetwork('1.2.3.0/24')
    description = 'Debogon-prefix'
    assert response.smallest_network == network
    print(response.description)
    assert response.description == description
    assert response.__repr__() == f'{network} {description}'
    for group in response.groups:
        assert group.is_empty is False
        assert isinstance(group.to_dict(), dict)


def test_whois_response_mock_domain():
    """
    Test loading WhoisQueryResponse from domain record data
    """
    response = get_empty_response()
    response.__load_data__(get_test_domain_lines(), [])
    assert response.__query_type__ == 'domain'
    for group in response.groups:
        assert group.is_empty is False
        assert isinstance(group.to_dict(), dict)
