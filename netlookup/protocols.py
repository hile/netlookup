"""
Parser for /etc/protocols file
"""
import re
from typing import List, Optional

from .base import FileItem, NetworkDataTextFile

PROTOCOLS_FILE_PATH = '/etc/protocols'

PROTOCOL_LINE_PATTERNS = (
    re.compile(r'^(?P<name>[^\s]+)\s+(?P<number>[^\s]+)\s+(?P<aliases>[^#]+)\s*$'),
    re.compile(r'^(?P<name>[^\s]+)\s+(?P<number>[^\s]+)\s+(?P<aliases>[^#]+)#(?P<comment>.*)$'),
)


class Protocol(FileItem):
    """
    Single protocol in the protocols file
    """
    __patterns__: List[re.Pattern] = PROTOCOL_LINE_PATTERNS

    def __init__(self,
                 name: str,
                 number: str,
                 aliases: str = '',
                 comment: str = '') -> None:
        self.name = name
        self.number = int(number)
        self.aliases = aliases
        self.comment = comment.strip()

    def __repr__(self):
        return f'{self.name} {self.number}'


class Protocols(NetworkDataTextFile):
    """
    Parser for /etc/protocols file
    """
    __item_loader__class__ = Protocol

    def __init__(self, path: Optional[str] = None):
        path = path if path is not None else PROTOCOLS_FILE_PATH
        super().__init__(path)
