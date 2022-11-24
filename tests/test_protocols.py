"""
Unit tests for netlookup.protocols module
"""
from netlookup.protocols import Protocols

PROTOCOLS_COUNT_DARWIN = 140
PROTOCOLS_COUNT_FREEBSD = 140
PROTOCOLS_COUNT_LINUX = 55
PROTOCOLS_COUNT_OPENBSD = 144


# pylint: disable=unused-argument
def test_protocols_load_darwin(mock_darwin_files):
    """
    Mock loading protocols for macOS Darwin
    """
    protocols = Protocols()
    assert len(protocols) == PROTOCOLS_COUNT_DARWIN


# pylint: disable=unused-argument
def test_protocols_load_freebsd(mock_freebsd_files):
    """
    Mock loading protocols for FreeBSD
    """
    protocols = Protocols()
    assert len(protocols) == PROTOCOLS_COUNT_FREEBSD


# pylint: disable=unused-argument
def test_protocols_load_linux(mock_linux_files):
    """
    Mock loading protocols for Linux
    """
    protocols = Protocols()
    assert len(protocols) == PROTOCOLS_COUNT_LINUX


# pylint: disable=unused-argument
def test_protocols_load_openbsd(mock_openbsd_files):
    """
    Mock loading protocols for OpenBSD
    """
    protocols = Protocols()
    assert len(protocols) == PROTOCOLS_COUNT_OPENBSD
