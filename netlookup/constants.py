"""
Constant values for netlookup module
"""
from pathlib import Path

NETLOOKUP_USER_DATA_PATH = Path('~/.config/netlookup').expanduser()

IPV4_VERSION = 4
IPV6_VERSION = 6

MAX_PREFIX_LEN_IPV4 = 32
MAX_PREFIX_LEN_IPV6 = 128
