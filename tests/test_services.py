#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.services module
"""
from netlookup.services import Service, Services

SERVICES_COUNT_DARWIN = 9886
SERVICES_COUNT_FREEBSD = 1939
SERVICES_COUNT_LINUX = 318
SERVICES_COUNT_OPENBSD = 304


def validate_service(service: Service) -> None:
    """
    Validate a single service object
    """
    assert isinstance(service, Service)
    assert isinstance(service.__repr__(), str)
    assert isinstance(service.port_number, int)
    assert isinstance(service.protocol, str)
    assert isinstance(service.name, str)
    assert isinstance(service.aliases, str)
    assert isinstance(service.comment, str)


def validate_services(services: Services, count: int) -> None:
    """
    Validate list of services
    """
    assert len(services) == count
    validate_service(services[-1])
    for service in services:
        validate_service(service)


# pylint: disable=unused-argument
def test_services_load_darwin(mock_darwin_files) -> None:
    """
    Mock loading services for macOS Darwin
    """
    validate_services(Services(), SERVICES_COUNT_DARWIN)


# pylint: disable=unused-argument
def test_services_load_freebsd(mock_freebsd_files) -> None:
    """
    Mock loading services for FreeBSD
    """
    validate_services(Services(), SERVICES_COUNT_FREEBSD)


# pylint: disable=unused-argument
def test_services_load_linux(mock_linux_files) -> None:
    """
    Mock loading services for Linux
    """
    validate_services(Services(), SERVICES_COUNT_LINUX)


# pylint: disable=unused-argument
def test_services_load_openbsd(mock_openbsd_files) -> None:
    """
    Mock loading services for OpenBSD
    """
    validate_services(Services(), SERVICES_COUNT_OPENBSD)
