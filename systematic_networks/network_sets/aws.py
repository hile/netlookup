
import json

from datetime import datetime
from operator import attrgetter

import requests

from ..network import NetworkError
from .base import NetworkSet, NetworkSetItem

AWS_IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
SKIP_SERVICE_NAMES = (
    'AMAZON',
)


class AWSPrefix(NetworkSetItem):
    """
    AWS network prefix with region and service details
    """
    type = 'aws'
    extra_attributes = ('region', 'services')

    def __init__(self, network, data=None):
        self.region = None
        self.services = []
        super().__init__(network, data)

    def __repr__(self):
        return f'{self.type} {self.region} {self.cidr}'


class AWS(NetworkSet):
    """
    AWS address networks
    """
    type = 'aws'
    cache_filename = 'aws-networks.json'
    loader_class = AWSPrefix

    @property
    def regions(self):
        """
        Return all detected regions
        """
        return sorted(set(prefix.region for prefix in self))

    @staticmethod
    def __get_aws_ip_ranges__():
        """
        Fetch AWS IP ranges
        """
        try:
            res = requests.get(AWS_IP_RANGES_URL)
            if res.status_code != 200:
                raise ValueError(f'HTTP status code {res.status_code}')
            return res.content
        except Exception as error:
            raise NetworkError(f'Error fetching AWS IP ranges: {error}')

    def fetch(self):
        """
        Fetch AWS IP range data
        """

        try:
            data = json.loads(self.__get_aws_ip_ranges__())
        except Exception as error:
            raise NetworkError(f'Error loading AWS IP range data: {error}')

        self.updated = datetime.fromtimestamp(int(data['syncToken']))
        networks = {}
        for item in data['prefixes']:
            prefix = self.loader_class(item['ip_prefix'], item)
            if prefix.cidr not in networks:
                networks[prefix.cidr] = prefix
            if item['service'] not in SKIP_SERVICE_NAMES and item['service'] not in networks[prefix.cidr].services:
                networks[prefix.cidr].services.append(item['service'])

        for item in data['ipv6_prefixes']:
            prefix = self.loader_class(item['ipv6_prefix'], item)
            if prefix.cidr not in networks:
                networks[prefix.cidr] = prefix
            if item['service'] not in SKIP_SERVICE_NAMES and item['service'] not in networks[prefix.cidr].services:
                networks[prefix.cidr].services.append(item['service'])

        for network in networks.values():
            self.__networks__.append(network)
        self.__networks__.sort(key=attrgetter('version', 'region', 'services', 'cidr'))
