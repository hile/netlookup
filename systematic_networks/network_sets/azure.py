
import json

from datetime import datetime
from operator import attrgetter

import requests

from ..network import NetworkError
from .base import NetworkSet, NetworkSetItem

AZURE_SERVICES_URL = 'https://azuredcip.azurewebsites.net/api/azuredcipranges'
AZURE_QUERY_DATA = json.dumps({'region': 'all', 'request': 'dcip'})


class AzurePrefix(NetworkSetItem):
    """
    Azure network prefix with region and service details
    """
    type = 'azure'
    extra_attributes = ('region',)

    def __init__(self, network, data=None):
        self.region = None
        super().__init__(network, data)

    def __repr__(self):
        return '{} {} {}'.format(self.type, self.region, self.cidr)

    def as_dict(self):
        """
        Return azure prefix with extra details
        """
        data = super().as_dict()
        data.update({
            'region': self.region,
        })
        return data


class Azure(NetworkSet):
    """
    Azure address networks
    """
    type = 'azure'
    cache_filename = 'azure-networks.json'
    loader_class = AzurePrefix

    @staticmethod
    def __get_azure_ip_ranges__():
        """
        Fetch Azure IP ranges
        """
        try:
            res = requests.post(
                AZURE_SERVICES_URL,
                data=AZURE_QUERY_DATA,
                headers={'Content-Type': 'application/json'}
            )
            if res.status_code != 200:
                raise ValueError('HTTP status code {}'.format(res.status_code))
            return res.content
        except Exception as error:
            raise NetworkError('Error fetching azure IP ranges: {}'.format(error))

    def fetch(self):
        """
        Fetch Azure IP range data
        """
        try:
            data = json.loads(self.__get_azure_ip_ranges__())
        except Exception as error:
            raise NetworkError('Error loading azure IP range data: {}'.format(error))

        self.__networks__.clear()
        for region in data:

            kwargs = {
                'region': region,
            }
            prefixes = data.get(region, [])
            if not prefixes:
                continue

            if isinstance(prefixes, str):
                prefixes = [prefixes]

            for prefix in prefixes:
                try:
                    self.__networks__.append(self.loader_class(prefix, kwargs))
                except Exception as error:
                    raise NetworkError(
                        'Error parsing region {} prefix "{}": {}'.format(
                            region,
                            data.get(region, []),
                            error
                        ))

        self.updated = datetime.now()
        self.__networks__.sort(key=attrgetter('region'))

        return data
