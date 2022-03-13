"""
Unit tests for netloookup.network_sets.configuration settings
"""

from pathlib import Path

from netlookup.network_sets.base import NetworkSet
from netlookup.prefixes import Prefixes
from netlookup.network_sets.configuration import (
    get_cache_directory,
    DARWIN_CACHE_DIRECTORY,
    DEFAULT_CACHE_DIRECTORY
)


def test_network_sets_configuration_default_cache_directory():
    """
    Test default cache directory attribute for network sets
    """
    network_set = NetworkSet()
    assert isinstance(network_set.cache_directory, Path)
    assert network_set.cache_directory == get_cache_directory()


def test_prefixes_configuration_default_cache_directory():
    """
    Test default cache directory attribute for prefixes
    """
    prefixes = Prefixes()
    assert isinstance(prefixes.cache_directory, Path)
    assert prefixes.cache_directory == get_cache_directory()


def test_prefixes_configuration_darwin_cache_directory(monkeypatch):
    """
    Test cache directory attribute for darwin platform
    """
    monkeypatch.setattr('sys.platform', 'darwin')
    prefixes = Prefixes()
    assert prefixes.cache_directory == DARWIN_CACHE_DIRECTORY


def test_prefixes_configuration_linux_cache_directory(monkeypatch):
    """
    Test cache directory attribute for linux platform
    """
    monkeypatch.setattr('sys.platform', 'linux')
    prefixes = Prefixes()
    assert prefixes.cache_directory == DEFAULT_CACHE_DIRECTORY
