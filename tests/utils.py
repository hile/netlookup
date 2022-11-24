"""
Utility methods for netlookup unit tests
"""

from netlookup.network import Network


def validate_network_compare_methods(network):
    """
    Validate a network object's compare methods
    """
    host = network.first_host
    if host is not None:
        assert network != str(host)
        assert network != host
        assert network < str(host)
        assert network < host
        assert network <= str(host)
        assert network <= host
        assert str(host) > network
        assert host > network
        assert str(host) >= network
        assert host >= network

    try:
        next_network = network.next()  # noqa
        assert next_network > network
        assert next_network >= network
    except IndexError:
        # Past network range max, this is ok
        pass


def validate_network(network):
    """
    Validate a network object
    """
    assert isinstance(network, Network)
    assert isinstance(network.__repr__(), str)
