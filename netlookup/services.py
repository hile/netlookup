#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Parser for /etc/services file
"""
import re

from typing import List, Optional

from .base import FileItem, NetworkDataTextFile

SERVICES_FILE_PATH = '/etc/services'

SERVICE_LINE_PATTERNS = (
    re.compile(
        r'^(?P<name>[^\s]+)\s+(?P<port_number>[^/]+)/(?P<protocol>[^\s]+)\s*$'
    ),
    re.compile(
        r'^(?P<name>[^\s]+)\s+(?P<port_number>[^/]+)/(?P<protocol>[^\s]+)'
        r'\s+#(?P<comment>.*)$'),
    re.compile(
        r'^(?P<name>[^\s]+)\s+(?P<port_number>[^/]+)/(?P<protocol>[^\s]+)'
        r'\s+(?P<aliases>[^#]+)\s*$'),
    re.compile(
        r'^(?P<name>[^\s]+)\s+(?P<port_number>[^/]+)/(?P<protocol>[^\s]+)'
        r'\s+(?P<aliases>[^#]+)\s+#(?P<comment>.*)$'
    ),
    re.compile(
        r'^(?P<port_number>[^/]+)/(?P<protocol>[^\s]+)\s*$'
    ),
    re.compile(
        r'^(?P<port_number>[^/]+)/(?P<protocol>[^\s]+)\s+'
        r'#(?P<comment>.*)$'
    ),
    re.compile(
        r'^(?P<port_number>[^/]+)/(?P<protocol>[^\s]+)\s+'
        r'(?P<aliases>[^#]+)\s*$'
    ),
    re.compile(
        r'^(?P<port_number>[^/]+)/(?P<protocol>[^\s]+)\s+'
        r'(?P<aliases>[^#]+)\s+#(?P<comment>.*)$'
    ),
)


class Service(FileItem):
    """
    Single service in the services file
    """
    __patterns__: List[re.Pattern] = SERVICE_LINE_PATTERNS

    def __init__(self,
                 port_number: str,
                 protocol: str,
                 name: str = '',
                 aliases: str = '',
                 comment: str = '') -> None:
        self.port_number = int(port_number)
        self.protocol = protocol
        self.name = name
        self.aliases = aliases.strip()
        self.comment = comment.strip()

    def __repr__(self) -> str:
        return f'{self.name} {self.port_number}/{self.protocol}'


class Services(NetworkDataTextFile):
    """
    Parser for /etc/services file
    """
    __item_loader__class__ = Service

    def __init__(self, path: Optional[str] = None):
        path = path if path is not None else SERVICES_FILE_PATH
        super().__init__(path)
