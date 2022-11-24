"""
Unit tests for netlookup.services module
"""
from netlookup.services import Services

SERVICES_COUNT_DARWIN = 9886
SERVICES_COUNT_FREEBSD = 1939
SERVICES_COUNT_LINUX = 318
SERVICES_COUNT_OPENBSD = 304


# pylint: disable=unused-argument
def test_services_load_darwin(mock_darwin_files):
    """
    Mock loading services for macOS Darwin
    """
    services = Services()
    assert len(services) == SERVICES_COUNT_DARWIN


# pylint: disable=unused-argument
def test_services_load_freebsd(mock_freebsd_files):
    """
    Mock loading services for FreeBSD
    """
    services = Services()
    assert len(services) == SERVICES_COUNT_FREEBSD


# pylint: disable=unused-argument
def test_services_load_linux(mock_linux_files):
    """
    Mock loading services for Linux
    """
    services = Services()
    assert len(services) == SERVICES_COUNT_LINUX


# pylint: disable=unused-argument
def test_services_load_openbsd(mock_openbsd_files):
    """
    Mock loading services for OpenBSD
    """
    services = Services()
    assert len(services) == SERVICES_COUNT_OPENBSD
