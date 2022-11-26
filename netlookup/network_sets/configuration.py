"""
Network setcache directory configuration
"""
import sys
from pathlib import Path

DARWIN_CACHE_DIRECTORY = Path('~/Library/Caches/netlookup').expanduser()
DEFAULT_CACHE_DIRECTORY = Path('~/.cache/netlookup').expanduser()


def get_cache_directory():
    """
    Return netlookup data cace directory
    """
    return DARWIN_CACHE_DIRECTORY if sys.platform == 'darwin' else DEFAULT_CACHE_DIRECTORY
