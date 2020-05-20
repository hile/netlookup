"""
Whois query response
"""

import json

from datetime import datetime
from operator import attrgetter

from netaddr.ip import IPAddress, AddrFormatError

from systematic_cli.base import Base
from systematic_cli.exceptions import ScriptError
from systematic_cli.process import run_command_lineoutput

from ..encoders import NetworkDataEncoder
from ..exceptions import WhoisQueryError

from .constants import ORGANIZATION_FIELDS
from .groups import InformationSectionGroup, GROUP_LOADERS
from .utils import parse_field_value

COMMENT_MARKERS = ('#%')
LINE_ENCODINGS = ('utf-8', 'latin1')
QUERY_TIMEOUT = 10


class WhoisQueryResponse(Base):
    """
    Query whois
    """
    __group_loaders__ = GROUP_LOADERS
    __fallback_group_loader__ = InformationSectionGroup

    def __init__(self, whois, debug_enabled=False, silent=False):
        super().__init__(debug_enabled=debug_enabled, silent=silent)
        self.__query_type__ = None
        self.__query__ = None
        self.__stdout__ = None
        self.__stderr__ = None
        self.whois = whois
        self.__loaded__ = None
        self.groups = []
        self.address_ranges = []
        self.networks = []

    def __repr__(self):
        if self.__query_type__ == 'address':
            return f'{self.smallest_network} {self.description}'
        if self.__query__ is not None:
            return self.__query__
        return str(self.__class__)

    @property
    def smallest_network(self):
        """
        Return smallest network for a response
        """
        if self.networks:
            return str(self.networks[0])
        return None

    # pylint: disable=too-many-nested-blocks
    @property
    def description(self):
        """
        Return description for a response
        """
        if self.networks:
            for section in ('route', 'inetnum', 'inet6num'):
                for group in reversed(self.groups):
                    if group.section != section:
                        continue
                    for field in ('network_name', 'description'):
                        value = group.get(field, None)
                        if value:
                            if isinstance(value, list):
                                return value[0]
                            return value
        for group in reversed(self.groups):
            if group.section in ORGANIZATION_FIELDS:
                organization = group.get('organization', None)
                if organization and isinstance(organization, list):
                    return ', '.join(organization)
                return organization
        return ''

    def __get_group_loader_class__(self, line):
        """
        Get loader class for specified section group type
        """
        field, value = parse_field_value(line)
        is_label = not value
        if field is None:
            return None, is_label
        for loader in self.__group_loaders__:
            if field in loader.__groups__:
                return loader, is_label
        self.debug(f'unmapped group {field}')
        return self.__fallback_group_loader__, is_label

    def __create_group__(self, line):
        """
        Create group
        """
        loader, is_label = self.__get_group_loader_class__(line)
        if loader is None:
            return None, is_label
        try:
            group = loader(self, line)
        except WhoisQueryError as error:
            self.debug(error)
            return None, is_label
        self.groups.append(group)
        return group, is_label

    def __stdout_item_iterator__(self):
        """
        Parse whois query data as iterator

        Triggers query if self.__stdout__ or self.__stderr__ is undefined
        """

        group = None
        is_label = False
        for line in self.__stdout__:
            comment = line[:1] in COMMENT_MARKERS
            if comment or line.strip() == '':
                has_data = group is not None and not group.is_empty
                if not is_label or is_label and has_data:
                    group = None
            elif group is None:
                group, is_label = self.__create_group__(line)
                if group is not None:
                    yield group

            if group is not None:
                group.parse_line(line)

    def __detect_networks__(self):
        """
        Detect network ranges and networks in groups
        """
        self.networks = []
        self.address_ranges = []

        for group in self.groups:
            for address_range in group.address_ranges:
                if address_range not in self.address_ranges:
                    self.address_ranges.append(address_range)
            for network in group.networks:
                if network not in self.networks:
                    self.networks.append(network)

        self.address_ranges.sort(key=attrgetter('size'))
        self.networks.sort(key=attrgetter('size'))

    @staticmethod
    def __detect_query_type__(query):
        """
        Detect query type
        """
        try:
            IPAddress(query)
            return 'address'
        except (ValueError, AddrFormatError):
            pass

        fields = query.split('.')
        for field in fields:
            if field == '' or len(field.split()) > 1:
                raise WhoisQueryError(f'invalid whois query {query}')
        return 'dns'

    def __load_data__(self, stdout, stderr, query_type=None, loaded_timestamp=None):
        """
        Load data from response
        """
        self.__stdout__ = stdout
        self.__stderr__ = stderr
        self.__query_type__ = query_type
        self.groups = []
        list(self.__stdout_item_iterator__())
        for group in self.groups:
            group.finalize()
        self.__detect_networks__()
        if loaded_timestamp is not None:
            self.__loaded__ = loaded_timestamp
        else:
            self.__loaded__ = datetime.now().timestamp()

        if self.__query_type__ is None:
            self.__query_type__ = 'address' if self.address_ranges is not None else 'dns'

    def query(self, query):
        """
        Run whois query for query value

        Stores response __stdout__ / __stderr__ lines to
        self.__stdout__ and self.__stderr__
        """
        query_type = self.__detect_query_type__(query)
        self.debug(f'whois query {query}')
        try:
            stdout, stderr = run_command_lineoutput(
                *('whois', str(query)),
                encodings=LINE_ENCODINGS,
                timeout=QUERY_TIMEOUT
            )
            self.__query__ = query
            self.__load_data__(stdout, stderr, query_type=query_type)
        except ScriptError as error:
            raise WhoisQueryError(error)

    def match(self, query):
        """
        Match query to smallest network in response

        Response usually contains the parent inetnum delegation which we
        don't want to match
        """
        query_type = self.__detect_query_type__(query)
        if query_type == 'address':
            if self.networks:
                return query in self.networks[0]
        if self.__query__:
            return self.__query__ == query
        return None

    def to_dict(self):
        """
        Return data as dictionary
        """
        return {
            'groups': self.groups,
        }

    def as_json(self):
        """
        Return whois query result as JSON
        """
        response = {}
        for group in self.groups:
            for key, value in group.to_dict().items():
                if key not in response:
                    response[key] = value
                elif not isinstance(response[key], list):
                    response[key] = [response[key]] + [value]
                else:
                    response[key].append(value)
        return json.dumps(response, indent=2, cls=NetworkDataEncoder)
