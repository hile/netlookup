"""
Whois query for IP addresses and DNS names
"""

import json

from datetime import datetime, timedelta
from pathlib import Path

from netaddr.ip import IPAddress

from sys_toolkit.base import LoggingBaseClass
from sys_toolkit.textfile import LineTextFile

from ..encoders import NetworkDataEncoder
from ..exceptions import WhoisQueryError

from .constants import RESPONSE_MAX_AGE_SECONDS, WhoisQueryType
from .response import PWhoisQueryResponse, WhoisQueryResponse
from .utils import parse_datetime

PREFIX_CACHE_FILE = Path('~/.config/netlookup/pwhois.json').expanduser()
WHOIS_CACHE_FILE = Path('~/.config/netlookup/whois.json').expanduser()


class QueryLookupCache(LoggingBaseClass):
    """
    Common base class for whois query lookup cachdes
    """
    def __init__(self, cache_file=None, debug_enabled=False, silent=False):
        super().__init__(debug_enabled=debug_enabled, silent=silent)
        self.cache_file = cache_file if cache_file is not None else self.__default_cache_file__
        self.__responses__ = []
        self.load_cache()

    def __load_json_record__(self, record):
        raise NotImplementedError

    def __format_json_data__(self):
        raise NotImplementedError

    @property
    def __default_cache_file__(self):
        return None

    def load_cache(self):
        """
        Load cached JSON data
        """
        if not self.cache_file or not self.cache_file.exists():
            return
        for record in json.loads(self.cache_file.read_text()):
            self.__responses__.append(self.__load_json_record__(record))

    def write_cache(self):
        """
        Write resolved entires to JSON cache file
        """
        if not self.cache_file:
            raise WhoisQueryError('Cache file is not defined')
        if not self.cache_file.parent.is_dir():
            self.cache_file.parent.mkdir(parents=True)
        with self.cache_file.open('w') as filedescriptor:
            filedescriptor.write(
                json.dumps(self.__format_json_data__(), indent=2, cls=NetworkDataEncoder)
            )

    def match(self, value, max_age=None):
        """
        Match specified value to existing responses
        """
        raise NotImplementedError

    def query(self, value, max_age=RESPONSE_MAX_AGE_SECONDS):
        """
        Query must be implemented in child class
        """
        raise NotImplementedError

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

    def __call__(self, value, max_age=RESPONSE_MAX_AGE_SECONDS):
        """
        Call whois query class as query method
        """
        return self.query(value, max_age)


class WhoisAddressLookup(QueryLookupCache):
    """
    Query whois for IP address details
    """
    def __init__(self, cache_file=None, debug_enabled=False, silent=False):
        self.__dns_lookup_table__ = {}
        self.__unmapped_fields__ = {}
        super().__init__(cache_file=cache_file, debug_enabled=debug_enabled, silent=silent)

    @property
    def __default_cache_file__(self):
        return WHOIS_CACHE_FILE

    def __load_json_record__(self, record):
        """
        Load a JSON record from cached data
        """
        query_type = record.get('query_type', None)
        query = record.get('query', None)
        loaded_timestamp = parse_datetime(record['loaded_timestamp']).timestamp()
        stdout = record['lines']
        response = WhoisQueryResponse(self, debug_enabled=self.__debug_enabled__, silent=self.__silent__)
        response.__load_data__(
            stdout=stdout,
            stderr=[],
            loaded_timestamp=loaded_timestamp,
            query_type=query_type
        )
        response.__query__ = query
        if query_type == WhoisQueryType.DOMAIN and query:
            self.__dns_lookup_table__[query] = response
        return response

    def __format_json_data__(self):
        """
        Format written data as JSON for saving to cache file
        """
        now = datetime.now().timestamp()
        return [
            {
                'query_type': response.__query_type__,
                'query': response.__query__,
                'loaded_timestamp': response.__loaded__ if response.__loaded__ else now,
                'lines': response.__stdout__,
            }
            for response in self.__responses__
        ]

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
            silent=self.__setattr__
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


class PrefixLookup(QueryLookupCache):
    """
    Route prefix lookup from pwhois service
    """
    @property
    def __default_cache_file__(self):
        return PREFIX_CACHE_FILE

    def __load_json_record__(self, record):
        return None

    def __format_json_data__(self):
        return {}

    def match(self, value, max_age=None):
        """
        Match a cached prefix lookup value
        """
        time_limit = None
        if max_age is not None:
            time_limit = (datetime.now() - timedelta(seconds=max_age)).timestamp()

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
        Query pwhois server for prefix informtation
        """
        response = self.match(value, max_age)
        if response is not None:
            return response

        response = PWhoisQueryResponse(
            self,
            debug_enabled=self.__debug_enabled__,
            silent=self.__setattr__)
        response.query(value)
        self.__responses__.append(response)
        try:
            self.write_cache()
        except Exception as error:
            self.debug(f'error updating cache file {self.cache_file}: {error}')
        return response
