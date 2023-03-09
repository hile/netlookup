#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
AWS address prefix set
"""
import json

from datetime import datetime
from http import HTTPStatus
from operator import attrgetter
from typing import List, Optional, Tuple, TYPE_CHECKING

import requests

from ..exceptions import NetworkError
from .base import NetworkSet, NetworkSetItem
from .constants import REQUEST_TIMEOUT

if TYPE_CHECKING:
    from ..network import Network

AWS_IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
SKIP_SERVICE_NAMES = (
    'AMAZON',
)


class AWSPrefix(NetworkSetItem):
    """
    AWS network prefix with region and service details
    """
    type: str = 'aws'
    network: 'Network'
    region: Optional[str]
    extra_attributes: Tuple[str] = ('region', 'services')

    def __init__(self, network: 'Network', data: dict = None):
        self.region = None
        self.services = []
        super().__init__(network, data)

    def __repr__(self) -> str:
        return f'{self.type} {self.region} {self.cidr}'


class AWS(NetworkSet):
    """
    AWS address networks
    """
    type: str = 'aws'
    cache_filename: str = 'aws-networks.json'
    loader_class = AWSPrefix

    @property
    def regions(self) -> List[str]:
        """
        Return all detected regions
        """
        return sorted(set(prefix.region for prefix in self))

    @staticmethod
    def __get_aws_ip_ranges__() -> str:
        """
        Fetch AWS IP ranges
        """
        try:
            res = requests.get(AWS_IP_RANGES_URL, timeout=REQUEST_TIMEOUT)
            if res.status_code != HTTPStatus.OK:
                raise NetworkError(f'HTTP status code {res.status_code}')
            return res.content
        except Exception as error:
            raise NetworkError(f'Error fetching AWS IP ranges: {error}') from error

    def fetch(self) -> None:
        """
        Fetch AWS IP range data
        """
        try:
            data = json.loads(self.__get_aws_ip_ranges__())
        except Exception as error:
            raise NetworkError(f'Error loading AWS IP range data: {error}') from error

        self.updated = datetime.fromtimestamp(int(data['syncToken']))

        networks = {}
        record_field_map = {
            'prefixes': 'ip_prefix',
            'ipv6_prefixes': 'ipv6_prefix',
        }
        for group, field in record_field_map.items():
            for item in data[group]:
                prefix = self.loader_class(item[field], item)
                if prefix.cidr not in networks:
                    networks[prefix.cidr] = prefix
                if item['service'] not in SKIP_SERVICE_NAMES and item['service'] not in networks[prefix.cidr].services:
                    networks[prefix.cidr].services.append(item['service'])

        self.__networks__ = []
        for network in networks.values():
            self.__networks__.append(network)

        self.__networks__.sort(key=attrgetter('version', 'region', 'services', 'cidr'))
