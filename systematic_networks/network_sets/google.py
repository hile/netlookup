
from datetime import datetime
from operator import attrgetter

from .base import NetworkSet, NetworkSetItem
from .utils import process_google_rr_ranges

ADDRESS_LIST_RECORD = '_spf.google.com'


class GoogleServicePrefix(NetworkSetItem):
    """
    Google services network prefix
    """
    type = 'google'


class GoogleServices(NetworkSet):
    """
    Google services address ranges

    Note: this data currently does not include information about regions
    """
    type = 'google'
    cache_filename = 'google-service-networks.json'
    loader_class = GoogleServicePrefix

    def fetch(self):
        """
        Feth google service ranges from DNS
        """
        self.__networks__.clear()
        for network in process_google_rr_ranges(ADDRESS_LIST_RECORD, self.loader_class):
            self.__networks__.append(network)
        self.updated = datetime.now()
        self.__networks__.sort(key=attrgetter('version', 'cidr'))
