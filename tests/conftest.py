"""
Unit test configuration for netlookup module
"""
from pathlib import Path

import pytest

from netlookup.prefixes import Prefixes

MOCK_DATA = Path(__file__).parent.joinpath('mock')
MOCK_PREFIXES_CACHE_DIRECTORY = MOCK_DATA.joinpath('prefixes/cache')


def mock_environment_services(monkeypatch, environment):
    """
    Mock loading of environment's /etc/services from mock data
    """
    monkeypatch.setattr(
        'netlookup.services.SERVICES_FILE_PATH',
        str(MOCK_DATA.joinpath(f'platform/{environment}/services'))
    )


def mock_environment_protocols(monkeypatch, environment):
    """
    Mock loading of environment's /etc/protocols from mock data
    """
    monkeypatch.setattr(
        'netlookup.protocols.PROTOCOLS_FILE_PATH',
        str(MOCK_DATA.joinpath(f'platform/{environment}/protocols'))
    )


@pytest.fixture
def mock_prefixes_cache() -> Prefixes:
    """
    Return prefixes object with cache path from mocked data
    """
    yield Prefixes(cache_directory=MOCK_PREFIXES_CACHE_DIRECTORY)


@pytest.fixture
def mock_darwin_files(monkeypatch):
    """
    Mock loading of /etc/services and /etc/platforms for macOS darwin
    """
    mock_environment_protocols(monkeypatch, 'darwin')
    mock_environment_services(monkeypatch, 'darwin')


@pytest.fixture
def mock_freebsd_files(monkeypatch):
    """
    Mock loading of /etc/services and /etc/platforms for FreeBSD
    """
    mock_environment_protocols(monkeypatch, 'freebsd')
    mock_environment_services(monkeypatch, 'freebsd')


@pytest.fixture
def mock_linux_files(monkeypatch):
    """
    Mock loading of /etc/services and /etc/platforms for Linux
    """
    mock_environment_protocols(monkeypatch, 'linux')
    mock_environment_services(monkeypatch, 'linux')


@pytest.fixture
def mock_openbsd_files(monkeypatch):
    """
    Mock loading of /etc/services and /etc/platforms for OpenBSD
    """
    mock_environment_protocols(monkeypatch, 'openbsd')
    mock_environment_services(monkeypatch, 'openbsd')
