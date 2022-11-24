"""
Common base classes for network info text file parsers
"""
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any, List, Optional


def match_patterns(patterns, line) -> Optional[dict]:
    """
    Parse fields in line with patterns
    """
    line = line.rstrip()
    for pattern in patterns:
        match = pattern.match(line)
        if match:
            return match.groupdict()
    raise ValueError(f'Error parsing line {line}')


# pylint: disable=too-few-public-methods
class FileItem:
    """
    Data item in the text file
    """
    __patterns__: List[re.Pattern] = []

    @classmethod
    def from_line(cls, line: str):
        """
        Parse a protocol from a line
        """
        match = match_patterns(cls.__patterns__, line)
        return cls(**match)


class NetworkDataTextFile(Sequence):
    """
    Text file with lines of network data, parsed per lined
    """
    __item_loader__class__ = FileItem

    def __init__(self, path: str) -> None:
        self.__items__ = self.__load__(Path(path))

    def __getitem__(self, key: str):
        return self.__items__.__getitem__(key)

    def __iter__(self):
        return iter(self.__items__)

    def __len__(self):
        return len(self.__items__)

    def __load__(self, path: Path) -> List[Any]:
        """
        Load items from the text data file
        """
        items = []
        with path.open('r', encoding='UTF-8') as handle:
            for line in handle.readlines():
                line = line.strip()
                if line == '' or line.startswith('#'):
                    continue
                items.append(self.__item_loader__class__.from_line(line))
        return items
