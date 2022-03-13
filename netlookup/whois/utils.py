"""
Utilities for whois lookups
"""

from datetime import datetime
import re

import inflection

from netaddr.ip import IPNetwork, IPRange, AddrFormatError

from ..exceptions import WhoisQueryError
from .constants import DATETIME_FORMATS, GLOBAL_FIELD_MAP, GLOBAL_FIELD_ALIASES

RE_FIELD = re.compile(r'^(?P<field>[a-zA-Z0-9_. -]+):\s+(?P<value>.*)$')
RE_LABEL = re.compile(r'^(?P<label>[A-Za-z]+)$')


def parse_datetime(value):
    """
    Parse date value
    """
    date = value
    if isinstance(value, float):
        return datetime.fromtimestamp(value)

    if date.endswith('Z'):
        date = f'{date[:-1]}+00:00'

    try:
        return datetime.fromisoformat(date)
    except ValueError:
        pass

    for datetime_format in DATETIME_FORMATS:
        try:
            return datetime.strptime(date, datetime_format)
        except ValueError:
            pass
    raise WhoisQueryError(f'Error parsing datetime value {value}')


def parse_field_value(line):
    """
    Format field name to underscore format
    """
    field = None
    value = None

    match = RE_FIELD.match(line)
    if match:
        field = match.groupdict()['field']
        value = match.groupdict()['value']
    else:
        match = RE_LABEL.match(line)
        if match:
            field = match.groupdict()['label']
            value = ''

    if not field:
        return None, None

    field = field.strip().rstrip('.').replace(' ', '_').replace('-', '_')
    field = inflection.underscore(field)
    return field, value.strip().rstrip(',').replace(',,', ',')


def lookup_field_alias(obj, field):
    """
    Look up field alias and additional details
    """
    for key, aliases in GLOBAL_FIELD_ALIASES.items():
        if field in aliases:
            field = key

    item = None
    if callable(getattr(obj, '__map_field_name__', None)):
        field = obj.__map_field_name__(field)

    if hasattr(obj, '__field_map__') and field in obj.__field_map__:
        item = obj.__field_map__[field]
    elif GLOBAL_FIELD_MAP.get(field, None) is not None:
        item = GLOBAL_FIELD_MAP[field]

    return field, item


def parse_network_value(value):
    """
    Parse IP range or IP network values
    """
    try:
        start, end = [arg.strip() for arg in value.split(' - ', 1)]
        try:
            return [IPRange(start, end)]
        except (AddrFormatError, ValueError) as error:
            raise WhoisQueryError(f'Error parsing network field value {value}: {error}') from error
    except ValueError:
        pass

    networks = []
    values = [arg.strip() for arg in value.split(',')]
    for item in values:
        try:
            networks.append(IPNetwork(item))
        except (AddrFormatError, ValueError) as error:
            raise WhoisQueryError(f'Error parsing network field value {value}: {error}') from error
    return networks
