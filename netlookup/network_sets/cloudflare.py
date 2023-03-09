#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Network set of cloudflare IP address ranges
"""
from datetime import datetime
from http import HTTPStatus
from operator import attrgetter
from typing import List

import requests

from ..exceptions import NetworkError
from .base import NetworkSet, NetworkSetItem
from .constants import REQUEST_TIMEOUT

CLOUDFLARE_IP_RANGES_IPV4_URL = 'https://www.cloudflare.com/ips-v4'
CLOUDFLARE_IP_RANGES_IPV6_URL = 'https://www.cloudflare.com/ips-v6'
CLOUDFLARE_IP_RANGES_IPV4_URLS = (
    CLOUDFLARE_IP_RANGES_IPV4_URL,
    CLOUDFLARE_IP_RANGES_IPV6_URL,
)


class CloudflarePrefix(NetworkSetItem):
    """
    Network prefix in cloudflare
    """
    type = 'cloudflare'


class Cloudflare(NetworkSet):
    """
    Network Set for cloudflare public addresses
    """
    type = 'cloudflare'
    cache_filename = 'cloudflare-networks.json'
    loader_class = CloudflarePrefix

    def __get_ip_range_data__(self, url: str) -> List[str]:
        """
        Cloudflare IP range data is available as text files from static URLs
        """
        try:
            res = requests.get(url, timeout=REQUEST_TIMEOUT)
            if res.status_code != HTTPStatus.OK:
                raise NetworkError(f'HTTP status code {res.status_code}')
            return str(res.content, encoding='utf-8').splitlines()
        except Exception as error:
            raise NetworkError(f'Error fetching Cloudflare IP ranges: {error}') from error

    def fetch(self) -> None:
        """
        Fetch and update cloudflare IP address ranges
        """
        self.updated = datetime.now()
        networks = {}

        for url in CLOUDFLARE_IP_RANGES_IPV4_URLS:
            prefixes = self.__get_ip_range_data__(url)
            for value in prefixes:
                prefix = self.loader_class(value)
                networks[prefix.cidr] = prefix

        self.__networks__ = []
        for network in networks.values():
            self.__networks__.append(network)

        self.__networks__.sort(key=attrgetter('cidr'))
