"""
Data format encoders
"""

from netaddr.ip import IPAddress, IPNetwork, IPRange

from systematic_cli.encoders import DateTimeEncoder


class NetworkDataEncoder(DateTimeEncoder):
    """
    JSON encoder with support for encoding:
    - dates, datetimes and timedeltas
    - networks
    - network adddresses
    - network routes
    """

    # pylint: disable=arguments-differ,method-hidden
    def default(self, obj):
        """
        Encode network objects as strings
        """
        if isinstance(obj, (IPAddress, IPNetwork, IPRange)):
            return str(obj)
        return super().default(obj)
