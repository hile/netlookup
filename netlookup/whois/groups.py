"""
Whois information section groups
"""

from datetime import datetime

from netaddr.ip import AddrFormatError, IPAddress, IPRange, IPNetwork

from ..exceptions import WhoisQueryError
from .constants import DATE_FIELDS, DATETIME_FIELDS, DOMAIN_FIELD_MAP, NETWORK_FIELDS
from .utils import lookup_field_alias, parse_datetime, parse_field_value, parse_network_value


class InformationSectionGroup(dict):
    """
    Group of details in information section
    """
    __section__ = None
    __groups__ = ()
    __field_map__ = {}
    __field_aliases__ = {}

    def __init__(self, query, line):
        super().__init__()
        self.query = query
        self.section = None
        self.networks = []
        self.address_ranges = []
        self.__descriptions__ = {}
        self.__parse_section_name__(line)

    def __map_field_name__(self, field):
        """
        Map handle fields to common fields
        """
        if not self.__field_aliases__:
            return field
        for key, aliases in self.__field_aliases__.items():
            if field in aliases:
                return key
        return field

    def __parse_section_name__(self, line):
        """
        Set section name for empty group
        """
        if self.__section__ is not None:
            self.section = self.__section__
        else:
            self.section, _value = parse_field_value(line)

    def __parse_field_name__(self, field):
        """
        Parse field name to unified format
        """
        field, item = lookup_field_alias(self, field)

        if item is not None:
            self.__descriptions__[field] = item['description']
        else:
            if field not in DATETIME_FIELDS and field not in DATE_FIELDS:
                self.query.whois.log_unmapped_field(self, field)
            self.__descriptions__[field] = ' '.join([
                item.capitalize()
                for item in field.replace('_', ' ').split()
            ])

        if item is not None and item.get('list_field', False) and field not in self:
            self[field] = []

        return field

    @property
    def is_empty(self):
        """
        Returns true if group is empty
        """
        if len(self.keys()) == 0:
            return True

        for value in self.values():
            if isinstance(value, list):
                if len(value) > 0:
                    return False
            else:
                return False
        return True

    @staticmethod
    def __parse_network_values__(value):
        """
        Parse network and address range values
        """
        values = parse_network_value(value)
        return values

    def __merge_network_data__(self, values):
        """
        Merge network values to self.address_ranges and self.networks
        """
        for value in values:
            if isinstance(value, IPRange):
                self.address_ranges.append(value)
                for network in value.cidrs():
                    if network not in self.networks:
                        self.networks.append(network)
            if isinstance(value, IPNetwork):
                self.networks.append(value)

    # pylint: disable=too-many-branches
    def parse_value(self, field, value):
        """
        Parse field value
        """
        field = self.__parse_field_name__(field)
        value = value.strip()

        if value and field in DATETIME_FIELDS or field in DATE_FIELDS:
            try:
                value = parse_datetime(value)
            except WhoisQueryError:
                try:
                    # Some 'changed' fields are prefixed with email
                    _prefix, value = value.split(None, 1)
                except ValueError:
                    pass
                try:
                    value = parse_datetime(value)
                except WhoisQueryError:
                    return
            if isinstance(value, datetime) and field in DATE_FIELDS:
                value = value.date()

        if field in NETWORK_FIELDS:
            value = self.__parse_network_values__(value)
            self.__merge_network_data__(value)

        if isinstance(value, list) and len(value) == 1:
            value = value[0]

        if value == '':
            return

        if field in self:
            if not isinstance(self[field], list):
                super().__setitem__(field, [self[field]])
            if isinstance(value, list):
                self[field].extend(value)
            else:
                self[field].append(value)
        else:
            self[field] = value

    def parse_line(self, line):
        """
        Parse line from data
        """
        field, value = parse_field_value(line)
        if field is not None:
            self.parse_value(field, value)

    def finalize(self):
        """
        Finalize field loading
        """

    def format_field_as_dict(self, key):
        """
        Format field as dict
        """
        return key, {
            'value': self[key],
            'description': self.__descriptions__.get(key, None),
        }

    def as_dict(self):
        """
        Return as dictionary
        """
        return {
            self.section: dict(
                self.format_field_as_dict(key)
                for key in self
            )
        }


class AddressMappedItem(InformationSectionGroup):
    """
    Item with address details
    """


class NetworkObject(InformationSectionGroup):
    """
    Object with network data
    """
    __field_map__ = {
        'mnt_lower': {
            'field': 'mnt_lower',
            'description': 'Maintainer of More Specific Routes',
        },
        'member_of': {
            'field': 'member_of_route_set',
            'description': 'Member of Route Set',
        }
    }

    def format_field_as_dict(self, key):
        """
        Format fields as dictionary
        """
        value = self[key]
        if isinstance(value, IPRange):
            return 'network_range', {
                'address_range': value,
                'networks': value.cidrs(),
                'description': 'Network Range',
                'size': value.size,
            }
        if isinstance(value, IPNetwork):
            return 'network', {
                'cidr': value,
                'description': 'Network',
                'size': value.size,
            }
        return super().format_field_as_dict(key)


class Changed(AddressMappedItem):
    """
    Record changed date details
    """
    __groups__ = [
        'changed',
    ]


class Contacts(AddressMappedItem):
    """
    Contact person
    """
    __section__ = 'contacts'
    __groups__ = [
        'contact',
    ]


class ContactPerson(AddressMappedItem):
    """
    Contact person
    """
    __section__ = 'contacts'
    __groups__ = [
        'person',
    ]


class CustomerName(AddressMappedItem):
    """
    Customer name
    """
    __groups__ = [
        'cust_name'
    ]


class Domain(AddressMappedItem):
    """
    Domain name
    """
    __groups__ = [
        'domain',
        'domain_name'
    ]
    __field_map__ = DOMAIN_FIELD_MAP


class DomainHolder(AddressMappedItem):
    """
    Domain holder
    """
    __groups__ = [
        'holder',
    ]
    __field_map__ = {
        'holder_email': {
            'field': 'domain_holder_email',
            'description': 'Email Address of Domain Holder'
        },
        'register_number': {
            'field': 'registeration_number',
            'description': 'Domain Registration Number'
        },
    }


class IncidentResponseTeam(AddressMappedItem):
    """
    Incident Response Team
    """
    __section__ = 'incident_response_team'
    __groups__ = [
        'irt'
    ]
    __field_map__ = {
        'auth': {
            'field': 'authorization',
            'description': 'IRT Authentication Scheme'
        },
        'irt': {
            'field': 'irt',
            'description': 'Incident Response Team',
        },
        'irt_nfy': {
            'field': 'irt_notification_email',
            'description': 'Incident Response Team Notification Email'
        },
    }


class InetNum(NetworkObject):
    """
    InetNum IPv4 network range
    """
    __groups__ = [
        'inetnum'
    ]
    __field_map__ = {
        'mnt_domains': {
            'field': 'maintainer_reverse_delegation',
            'description': 'Maintainer of Reverse Delegations'
        },
        'mnt_irt': {
            'field': 'maintainer_incident_response_team',
            'description': 'Maintainer of Incident Response Team'
        },
        'mnt_lower': {
            'field': 'maintainer_child_routes',
            'description': 'Maintainer of Child Routes'
        },
        'mnt_routes': {
            'field': 'maintainer_routes',
            'description': 'Maintainer of Routes'
        },
        'nslastaa': {
            'field': 'dns_server_last_ok_status',
            'description': 'Date of Latest DNS Server OK Status'
        },
        'nsstat': {
            'field': 'dns_server_status',
            'description': 'Status of DNS server'
        }
    }


class Inet6Num(NetworkObject):
    """
    Inet6Num IPv6 network range
    """
    __groups__ = [
        'inet6num'
    ]
    __field_map__ = {
        'assignment_size': {
            'field': 'assignment_size',
            'description': 'IPv6 Address Assignment Size'
        }
    }


class Nameservers(AddressMappedItem):
    """
    Nameserver for domain
    """
    __section__ = 'nameservers'
    __groups__ = [
        'nserver'
    ]
    __field_map__ = {
        'ds_rdata': {
            'field': 'delegation_signer_rr_data',
            'description': 'Delegation Signer Resouurce Record'
        },
    }

    def parse_nameserver(self, field, value):
        """
        Parse nameserver entry
        """
        field = self.__parse_field_name__(field)
        value = value.strip()
        try:
            hostname, addresses = value.split(None, 1)
            if not self[field]:
                self[field] = []
            self[field].append({
                'hostname': hostname,
                'addresses': [
                    IPAddress(address.strip())
                    for address in addresses.split()
                ],
            })
        except (ValueError, AddrFormatError):
            # Sometimes there is only hostname
            super().parse_value(field, value)

    def parse_value(self, field, value):
        """
        Parse nameservers group value
        """
        if field in self.__groups__:
            return self.parse_nameserver(field, value)
        return super().parse_value(field, value)


class NetworkRange(NetworkObject):
    """
    Network range
    """
    __groups__ = [
        'net_range',
    ]


class NicHandle(AddressMappedItem):
    """
    NIC handle
    """
    __groups__ = [
        'nic_handle'
    ]


class Organization(AddressMappedItem):
    """
    Organization information
    """
    __groups__ = [
        'organisation',
        'organization',
        'org_name'
    ]
    __field_map__ = {
        'mnt_ref': {
            'field': 'maintainer_ref',
            'description': 'Maintainer Reference',
        }
    }


class OrganizationContact(AddressMappedItem):
    """
    Organization contact handle
    """
    __groups__ = [
        'nic_handle',
        'nic_hdl',
        'nic_hdl_br',
        'org_abuse_handle',
        'org_noc_handle',
        'org_routing_handle',
        'org_tech_handle',
        'r_abuse_handle',
        'rnoc_handle',
        'r_tech_handle',
    ]
    __field_map__ = {
        'mnt_domains': {
            'field': 'mnt_domains',
            'description': 'Reverse Delegation Maintainer Authorizations'
        }
    }


class ReferralServer(InformationSectionGroup):
    """
    Whois server reference
    """
    __groups__ = [
        'refer',
        'referral_server',
    ]


class Registrar(AddressMappedItem):
    """
    DNS domain registrar
    """
    __groups__ = [
        'registrar'
    ]
    __field_aliases__ = {
        'registrar_url': {
            'www',
            'website',
        }
    }
    __field_map__ = {
        'registrar_url': {
            'field': 'registrar_url',
            'description': 'Registrar URL',
        }
    }


class Remarks(AddressMappedItem):
    """
    Role
    """
    __groups__ = [
        'remarks'
    ]


class ResourceLink(InformationSectionGroup):
    """
    Resource link
    """
    __groups__ = [
        'resource_link',
    ]


class Role(AddressMappedItem):
    """
    Role
    """
    __groups__ = [
        'role'
    ]


class Route(NetworkObject):
    """
    Details for a route
    """
    __groups__ = [
        'route',
    ]


class WhoisServer(InformationSectionGroup):
    """
    Whois response
    """
    __groups__ = [
        'whois',
    ]


GROUP_LOADERS = (
    Changed,
    ContactPerson,
    Contacts,
    CustomerName,
    Domain,
    DomainHolder,
    IncidentResponseTeam,
    Inet6Num,
    InetNum,
    Nameservers,
    NetworkRange,
    NicHandle,
    Organization,
    OrganizationContact,
    ReferralServer,
    Registrar,
    Remarks,
    ResourceLink,
    Role,
    Route,
    WhoisServer,
)
