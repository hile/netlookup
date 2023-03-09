#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.protocols module
"""
from netlookup.protocols import Protocol, Protocols

PROTOCOLS_COUNT_DARWIN = 140
PROTOCOLS_COUNT_FREEBSD = 140
PROTOCOLS_COUNT_LINUX = 55
PROTOCOLS_COUNT_OPENBSD = 144


def validate_protocol(protocol: Protocol) -> None:
    """
    Validate a single service object
    """
    assert isinstance(protocol, Protocol)
    assert isinstance(protocol.__repr__(), str)
    assert isinstance(protocol.name, str)
    assert isinstance(protocol.number, int)
    assert isinstance(protocol.aliases, str)
    assert isinstance(protocol.comment, str)


def validate_protocols(protocols: Protocols, count: int) -> None:
    """
    Validate Protocols object data
    """
    assert len(protocols) == count
    validate_protocol(protocols[-1])
    for protocol in protocols:
        validate_protocol(protocol)


# pylint: disable=unused-argument
def test_protocols_load_darwin(mock_darwin_files):
    """
    Mock loading protocols for macOS Darwin
    """
    validate_protocols(Protocols(), PROTOCOLS_COUNT_DARWIN)


# pylint: disable=unused-argument
def test_protocols_load_freebsd(mock_freebsd_files):
    """
    Mock loading protocols for FreeBSD
    """
    validate_protocols(Protocols(), PROTOCOLS_COUNT_FREEBSD)


# pylint: disable=unused-argument
def test_protocols_load_linux(mock_linux_files):
    """
    Mock loading protocols for Linux
    """
    validate_protocols(Protocols(), PROTOCOLS_COUNT_LINUX)


# pylint: disable=unused-argument
def test_protocols_load_openbsd(mock_openbsd_files):
    """
    Mock loading protocols for OpenBSD
    """
    validate_protocols(Protocols(), PROTOCOLS_COUNT_OPENBSD)
