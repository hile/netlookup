"""
Google Cloud address prefix set
"""
from datetime import datetime
from operator import attrgetter

from .base import NetworkSet, NetworkSetItem
from .utils import process_google_rr_ranges

ADDRESS_LIST_RECORD = '_cloud-netblocks.googleusercontent.com'


class GCPPrefix(NetworkSetItem):
    """
    GCP cloud network prefix
    """
    type = 'gcp'


class GCP(NetworkSet):
    """
    Google computing platform address ranges

    Note: this data currently does not include information about regions
    """
    type = 'gcp'
    cache_filename = 'gcp-networks.json'
    loader_class = GCPPrefix

    def fetch(self) -> None:
        """
        Fetch GCP network records from DNS
        """
        self.__networks__.clear()
        for network in process_google_rr_ranges(ADDRESS_LIST_RECORD, self.loader_class):
            self.__networks__.append(network)
        self.updated = datetime.now()
        self.__networks__.sort(key=attrgetter('version', 'cidr'))
