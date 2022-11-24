"""
Unit tests for netlookup.prefixes module
"""
from netlookup.prefixes import Prefixes

from .constants import MOCK_PREFIXES_CACHE_LEN


def test_prefixes_cache_load(mock_prefixes_cache) -> None:
    """
    Test loading cached prefixes from mocked data, ensure the number of
    prefixes is correct
    """
    assert isinstance(mock_prefixes_cache, Prefixes)
    assert len(mock_prefixes_cache) == MOCK_PREFIXES_CACHE_LEN
