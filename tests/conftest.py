"""
Unit test settings
"""

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def mock_whois_cache_path(monkeypatch, tmpdir):
    """
    Mock whois cache file path to avoid using existing caches
    """
    print('mock whois lookup cache file')
    monkeypatch.setattr(
        'netlookup.whois.lookup.WHOIS_CACHE_FILE',
        Path(tmpdir, 'whois.json')
    )
