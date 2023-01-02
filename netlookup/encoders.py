"""
Data format encoders
"""
from typing import Any

from netaddr.ip import IPAddress, IPNetwork, IPRange

from sys_toolkit.encoders import DateTimeEncoder


class NetworkDataEncoder(DateTimeEncoder):
    """
    JSON encoder with support for encoding:
    - dates, datetimes and timedeltas
    - networks
    - network adddresses
    - network routes
    """

    def default(self, o: Any):
        """
        Encode network objects as strings
        """
        if isinstance(o, (IPAddress, IPNetwork, IPRange)):
            return str(o)
        return super().default(o)
