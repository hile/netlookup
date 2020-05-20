#!/usr/bin/env python3
"""
Whois query for IP addresses and DNS names
"""

import json

from datetime import datetime, timedelta
from pathlib import Path

from netaddr.ip import IPAddress

from systematic_cli.base import Base
from systematic_cli.file import LineTextFile

from ..encoders import NetworkDataEncoder
from ..exceptions import WhoisQueryError

from .constants import RESPONSE_MAX_AGE_SECONDS
from .response import WhoisQueryResponse
from .utils import parse_datetime

DEFAULT_CACHE_FILE = Path('~/.config/whois.json').expanduser()


class WhoisAddressLookup(Base):
    """
    Query whois for IP address details
    """
    def __init__(self, cache_file=None, debug_enabled=False, silent=False):
        super().__init__(debug_enabled=debug_enabled, silent=silent)
        self.cache_file = cache_file if cache_file is not None else DEFAULT_CACHE_FILE
        self.__responses__ = []
        self.__dns_lookup_table__ = {}
        self.__unmapped_fields__ = {}
        self.load_cache()

    def log_unmapped_field(self, group, field):
        """
        Store unmapped fields and log to debug log
        """
        section = group.section
        if not section or field == group.section:
            return
        if section not in self.__unmapped_fields__:
            self.__unmapped_fields__[section] = []
        table = self.__unmapped_fields__[section]
        if field not in table:
            self.debug(f'unmapped field {type(group)} {section} {field}')
            table.append(field)

    def load_cache(self):
        """
        Load cached JSON data
        """
        if self.cache_file.exists():
            with self.cache_file.open('r') as filedescriptor:
                records = json.loads(filedescriptor.read())
            for record in records:
                query_type = record.get('query_type', None)
                query = record.get('query', None)
                loaded_timestamp = parse_datetime(record['loaded_timestamp']).timestamp()
                stdout = record['lines']
                response = WhoisQueryResponse(
                    self,
                    debug_enabled=self.__debug_enabled__,
                    silent=self.__silent__,
                )
                response.__load_data__(
                    stdout=stdout,
                    stderr=[],
                    loaded_timestamp=loaded_timestamp,
                    query_type=query_type
                )
                response.__query__ = query
                if query_type == 'dns' and query:
                    self.__dns_lookup_table__[query] = response
                self.__responses__.append(response)

    def write_cache(self):
        """
        Write resolved entires to JSON cache file
        """
        now = datetime.now().timestamp()
        data = [
            {
                'query_type': response.__query_type__,
                'query': response.__query__,
                'loaded_timestamp': response.__loaded__ if response.__loaded__ else now,
                'lines': response.__stdout__,
            }
            for response in self.__responses__
        ]
        with self.cache_file.open('w') as filedescriptor:
            filedescriptor.write(json.dumps(data, indent=2, cls=NetworkDataEncoder))

    def resolve_address_list_file(self, path):
        """
        Load file with lines of addresses and resolve them
        """
        path = Path(path).expanduser()
        for line in LineTextFile(path):
            if not self.match(line):
                try:
                    self.query(line)
                except WhoisQueryError as error:
                    self.error(error)
        self.write_cache()

    def match(self, value, max_age=None):
        """
        Match value to existing responses

        Returns response section or None
        """
        time_limit = None
        if max_age is not None:
            time_limit = (datetime.now() - timedelta(seconds=max_age)).timestamp()

        if not isinstance(value, IPAddress):
            try:
                value = IPAddress(value)
            except Exception:
                pass

        if value in self.__dns_lookup_table__:
            return self.__dns_lookup_table__[value]

        for response in self.__responses__:
            if not response.__loaded__:
                continue
            if time_limit is not None and response.__loaded__ < time_limit:
                continue
            if response.match(value):
                return response
        return None

    def query(self, value, max_age=RESPONSE_MAX_AGE_SECONDS):
        """
        Query value from whois

        Match to existing responses before sending request
        """
        response = self.match(value, max_age)
        if response is not None:
            return response

        response = WhoisQueryResponse(
            self,
            debug_enabled=self.__debug_enabled__,
            silent=self.__setattr__,
        )
        response.query(value)
        if not response.groups:
            raise WhoisQueryError('Whois query returns no data')
        self.__responses__.append(response)
        try:
            self.write_cache()
        except Exception as error:
            self.debug(f'error updating cache file {self.cache_file}: {error}')
        return response

    def filter_keys(self, key):
        """
        Return values for specified group key
        """
        matches = []
        for response in self.__responses__:
            for group in response.groups:
                if key in group:
                    self.debug(f'{group} {group[key]}')
                    matches.append(group[key])
        return matches

    def __call__(self, value, max_age=RESPONSE_MAX_AGE_SECONDS):
        """
        Call whois query class as query method
        """
        return self.query(value, max_age)
