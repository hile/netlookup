#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Google services address prefix set
"""
import re

from datetime import datetime
from operator import attrgetter
from typing import Optional

from dns import resolver

from ..exceptions import NetworkError
from .base import NetworkSet, NetworkSetItem

RE_INCLUDE = re.compile(r'^include:(?P<rr>.*)$')
RE_IPV4 = re.compile(r'^ip4:(?P<prefix>.*)$')
RE_IPV6 = re.compile(r'^ip6:(?P<prefix>.*)$')

GOOGLE_CLOUD_ADDRESS_LIST_RECORD = '_cloud-netblocks.googleusercontent.com'
GOOGLE_SERVICES_ADDRESS_LIST_RECORD = '_spf.google.com'


def google_rr_dns_query(record: str) -> Optional[str]:
    """
    DNS query to get TXT record list of google networks
    """
    try:
        res = resolver.resolve(record, 'TXT')
        return str(res.rrset[0].strings[0], 'utf-8')
    except (resolver.NoAnswer, resolver.NXDOMAIN) as error:
        raise NetworkError(f'Error querying TXT record for {record}: {error}') from error


def process_google_rr_ranges(record: str, loader_class):
    """
    Process RR records from google DNS query response
    """
    networks = []
    includes = []

    for field in google_rr_dns_query(record).split(' '):
        match = RE_IPV4.match(field)
        if match:
            networks.append(loader_class(match.groupdict()['prefix']))
            continue

        match = RE_IPV6.match(field)
        if match:
            networks.append(loader_class(match.groupdict()['prefix']))
            continue

        match = RE_INCLUDE.match(field)
        if match:
            include = match.groupdict()['rr']
            networks.extend(
                process_google_rr_ranges(include, loader_class)
            )
            includes.append(include)
            continue

    return networks


class GoogleNetworkSet(NetworkSet):
    """
    Google network set with data for TXT DNS records
    """
    @property
    def __address_list_record__(self) -> None:
        raise NotImplementedError

    def fetch(self) -> None:
        """
        Fetch Google Cloud network records from DNS
        """
        self.__networks__.clear()
        networks = process_google_rr_ranges(self.__address_list_record__, self.loader_class)
        for network in networks:
            self.__networks__.append(network)
        self.updated = datetime.now()
        self.__networks__.sort(key=attrgetter('version', 'cidr'))


class GoogleCloudPrefix(NetworkSetItem):
    """
    Google cloud network prefix
    """
    type = 'google-cloud'


class GoogleCloud(GoogleNetworkSet):
    """
    Google Cloud address ranges
    """
    type: str = 'google-cloud'
    cache_filename: str = 'google-cloud-networks.json'
    loader_class = GoogleCloudPrefix

    @property
    def __address_list_record__(self) -> str:
        return GOOGLE_CLOUD_ADDRESS_LIST_RECORD


class GoogleServicePrefix(NetworkSetItem):
    """
    Google services network prefix
    """
    type = 'google'


class GoogleServices(GoogleNetworkSet):
    """
    Google services address ranges
    """
    type: str = 'google'
    cache_filename: str = 'google-service-networks.json'
    loader_class = GoogleServicePrefix

    @property
    def __address_list_record__(self) -> str:
        return GOOGLE_SERVICES_ADDRESS_LIST_RECORD
