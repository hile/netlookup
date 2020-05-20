"""
Constants for whois lookups
"""

RESPONSE_MAX_AGE_SECONDS = 86400

DATE_FIELDS = (
    'creation_date',
    'expiry_date',
    'last_update',
    'last_updated',
    'modified',
    'nslastaa',
    'registered',
    'reg_date',
    'registry_expiry_date',
    'updated_date',
)

DATETIME_FIELDS = (
    'changed',
    'created',
    'expires',
    'last_modified',
    'updated',
)
DATETIME_FORMATS = (
    '%Y-%m-%dT%H:%M:%SZ',
    '%d.%m.%Y %H:%M:%S',
    '%d-%b-%Y',
    '%Y%m%d',
    '%Y-%m',
)

NETWORK_FIELDS = (
    'cidr',
    'cidr_address',
    'inetnum',
    'inet6num',
    'inetnum_up',
    'net_range',
    'reverse_route',
    'route',
)

ORGANIZATION_FIELDS = (
    'organization',
    'organisation',
    'org'
)

GLOBAL_FIELD_MAP = {
    'address': {
        'field': 'address',
        'description': 'Postal Address',
        'list_field': True,
    },
    'abuse_c': {
        'field': 'abuse_contact',
        'description': 'Abuse Contact',
    },
    'abuse_mailbox': {
        'field': 'abuse_mailbox',
        'description': 'Abuse Mailbox',
    },
    'admin_c': {
        'field': 'admin_contact',
        'description': 'Admin Contact',
    },
    'billing_c': {
        'field': 'billing_contact',
        'description': 'Billing Contact',
    },
    'cidr': {
        'field': 'cidr_address',
        'description': 'CIDR Address',
    },
    'city': {
        'field': 'city',
        'description': 'City',
    },
    'comment': {
        'field': 'comment',
        'description': 'Comments',
    },
    'contact': {
        'field': 'contact',
        'description': 'Contact Information',
    },
    'country': {
        'field': 'country_code',
        'description': 'Country Code',
    },
    'customer': {
        'field': 'customer',
        'description': 'Customer',
    },
    'descr': {
        'field': 'description',
        'description': 'Description',
    },
    'email': {
        'field': 'email',
        'description': 'Email Address',
    },
    'fax_no': {
        'field': 'fax_number',
        'description': 'Fax Number',
    },
    'geoloc': {
        'field': 'geoloc',
        'description': 'Geological Location',
    },
    'handle': {
        'field': 'handle',
        'description': 'Handle',
    },
    'inetrev': {
        'field': 'reverse_network',
        'description': 'Reverse Network',
    },
    'language': {
        'field': 'language',
        'description': 'Language',
    },
    'mnt_by': {
        'field': 'maintainer',
        'description': 'Maintainer',
    },
    'network_name': {
        'field': 'network_name',
        'description': 'Network Name',
    },
    'net_handle': {
        'field': 'network_handle',
        'description': 'Network Handle',
    },
    'net_type': {
        'field': 'network_type',
        'description': 'Network Allocation Type',
    },
    'nic_hdl': {
        'field': 'nic_handle',
        'description': 'NIC Handle',
    },
    'name': {
        'field': 'name',
        'description': 'Name',
    },
    'nameservers': {
        'field': 'nameservers',
        'description': 'DNS nameservers',
        'list_field': True,
    },
    'notify': {
        'field': 'notify_email',
        'description': 'Notifications Email Address',
    },
    'origin_as': {
        'field': 'origin_as',
        'description': 'Origin AS',
    },
    'org_id': {
        'field': 'organisation_id',
        'description': 'Organization ID',
    },
    'org_type': {
        'field': 'organisation_type',
        'description': 'Organization Type',
    },
    'organization': {
        'field': 'organization',
        'description': 'Organization',
    },
    'owner_c': {
        'field': 'owner_c',
        'description': 'Owner Contact',
    },
    'ownerid': {
        'field': 'owner_id',
        'description': 'Owner ID',
    },
    'parent': {
        'field': 'parent',
        'description': 'Parent',
    },
    'inetnum_up': {
        'field': 'parent_inetnum',
        'description': 'Parent Inetnum',
    },
    'phone': {
        'field': 'phone',
        'description': 'Phone Number',
    },
    'postal_code': {
        'field': 'postal_code',
        'description': 'Postal Code',
    },
    'reference': {
        'field': 'references',
        'description': 'References',
        'list_field': True,
    },
    'remarks': {
        'field': 'remarks',
        'description': 'Remarks',
        'list_field': True,
    },
    'resource_link': {
        'field': 'resource_link',
        'description': 'Resource Links',
        'list_field': True,
    },
    'source': {
        'field': 'source',
        'description': 'Source',
    },
    'sponsoring_org': {
        'field': 'sponsoring_organization',
        'description': 'Sponsoring Organization',
    },
    'state_prov': {
        'field': 'state',
        'description': 'State',
    },
    'status': {
        'field': 'status',
        'description': 'Status',
    },
    'tech_c': {
        'field': 'technical_contact',
        'description': 'Technical Contact',
    },
}

GLOBAL_FIELD_ALIASES = {
    'email': (
        'e_mail',
        'org_abuse_email',
        'org_noc_email',
        'org_routing_email',
        'org_tech_email',
        'r_tech_email',
        'rnoc_email',
        'r_abuse_email',
    ),
    'handle': (
        'org_abuse_handle',
        'org_noc_handle',
        'org_routing_handle',
        'org_tech_handle',
        'r_tech_handle',
        'rnoc_handle',
        'r_abuse_handle',
    ),
    'name': (
        'person',
        'org_abuse_name',
        'org_noc_name',
        'org_routing_name',
        'org_tech_name',
        'owner',
        'r_tech_name',
        'r_abuse_name',
        'responsible',
        'rnoc_name',
    ),
    'nameservers': {
        'nserver',
        'name_server',
    },
    'network_name': {
        'netname',
        'net_name',
    },
    'organization': (
        'org',
        'organisation',
        'org_name',
    ),
    'origin_as': (
        'aut_num',
        'origin',
    ),
    'phone': (
        'org_abuse_phone',
        'org_noc_phone',
        'org_routing_phone',
        'org_tech_phone',
        'r_tech_phone',
        'rnoc_phone',
        'r_abuse_phone',
    ),
    'reference': {
        'ref',
        'org_abuse_ref',
        'org_noc_ref',
        'org_routing_ref',
        'org_tech_ref',
        'r_tech_ref',
        'rnoc_ref',
        'r_abuse_ref',
    }
}

DOMAIN_FIELD_MAP = {
    'available': {
        'field': 'available',
        'description': 'Is Domain Available',
    },
    'admin_city': {
        'field': 'admin_address_city',
        'description': 'Administrative Contact City',
    },
    'admin_country': {
        'field': 'admin_address_country',
        'description': 'Administrative Contact Country',
    },
    'admin_email': {
        'field': 'admin_contact_email',
        'description': 'Administrative Contact Email',
    },
    'admin_fax': {
        'field': 'admin_contact_fax',
        'description': 'Administrative Contact Fax Number',
    },
    'admin_fax_ext': {
        'field': 'admin_contact_fax_external',
        'description': 'Administrative Contact Fax Number External',
    },
    'admin_name': {
        'field': 'admin_contact',
        'description': 'Administrative Contact',
    },
    'admin_phone': {
        'field': 'admin_contact_phone',
        'description': 'Administrative Contact Phone Number',
    },
    'admin_phone_ext': {
        'field': 'admin_contact_phone_external',
        'description': 'Administrative Contact Phone Number External',
    },
    'admin_organization': {
        'field': 'admin_organization',
        'description': 'Administrative Contact Organization',
    },
    'admin_postal_code': {
        'field': 'admin_address_postal_code',
        'description': 'Administrative Contact Postal Code',
    },
    'admin_street': {
        'field': 'admin_address_street_address',
        'description': 'Administrative Contact Street Address',
    },
    'dnssec': {
        'field': 'dnssec_enabled',
        'description': 'DNSSEC Enabled',
    },
    'domain_status': {
        'field': 'domain_status',
        'description': 'Domain Registration Status',
    },
    'hold': {
        'field': 'domain_hold_status',
        'description': 'Domain Hold Status',
    },
    'holder_c': {
        'field': 'domain_holder_contact',
        'description': 'Domain Holder',
    },
    'registrant_city': {
        'field': 'registrant_address_city',
        'description': 'Registrant Contact City',
    },
    'registrant_country': {
        'field': 'registrant_address_country',
        'description': 'Registrant Contact Country',
    },
    'registrant_email': {
        'field': 'registrant_contact_email',
        'description': 'Registrant Contact Email',
    },
    'registrant_fax': {
        'field': 'registrant_contact_fax',
        'description': 'Registrant Contact Fax Number',
    },
    'registrant_fax_ext': {
        'field': 'registrant_contact_fax_external',
        'description': 'Registrant Contact Fax Number External',
    },
    'registrant_name': {
        'field': 'registrant_contact',
        'description': 'Registrant Contact',
    },
    'registrant_phone': {
        'field': 'registrant_contact_phone',
        'description': 'Registrant Contact Phone Number',
    },
    'registrant_phone_ext': {
        'field': 'registrant_contact_phone_external',
        'description': 'Registrant Contact Phone Number External',
    },
    'registrant_organization': {
        'field': 'registrant_organization',
        'description': 'Registrant Contact Organization',
    },
    'registrant_postal_code': {
        'field': 'registrant_address_postal_code',
        'description': 'Registrant Contact Postal Code',
    },
    'registrant_street': {
        'field': 'registrant_address_street_address',
        'description': 'Registrant Contact Street Address',
    },
    'registrar': {
        'field': 'registrar',
        'description': 'Registrar Name',
    },
    'registrar_whois_server': {
        'field': 'registrar_whois_server',
        'description': 'Registrar Whois Server',
    },
    'registrar_url': {
        'field': 'registrar_url',
        'description': 'Registrar URRL',
    },
    'registrar_iana_id': {
        'field': 'registrar_iana_id',
        'description': 'Registrar IANA ID',
    },
    'registrar_abuse_contact_email': {
        'field': 'registrar_abuse_contact_email',
        'description': 'Registrar Abuse Contact Email',
    },
    'registrar_abuse_contact_phone': {
        'field': 'registrar_abuse_contact_phone',
        'description': 'Registrar Abuse Contact Phone',
    },
    'registrar_registration_expiration_date': {
        'field': 'registrar_registration_expiration_date',
        'description': 'Registrar Registration Expiration Date',
    },
    'registry_admin_id': {
        'field': 'registry_administrator_id',
        'description': 'Registy Administrator ID',
    },
    'registry_domain_id': {
        'field': 'registry_domain_id',
        'description': 'Registry Domain ID',
    },
    'registry_lock': {
        'field': 'registry_locked',
        'description': 'Registry Lock Status',
    },
    'registry_registrant_id': {
        'field': 'registry_registrant_id',
        'description': 'Registrar Registrant ID',
    },
    'registry_tech_id': {
        'field': 'registry_technical_contact_id',
        'description': 'Registry Technical Contact IDD',
    },
    'tech_city': {
        'field': 'technical_address_city',
        'description': 'Technical Contact City',
    },
    'tech_country': {
        'field': 'technical_address_country',
        'description': 'Technical Contact Country',
    },
    'tech_email': {
        'field': 'technical_contact_email',
        'description': 'Technical Contact Email',
    },
    'tech_fax': {
        'field': 'technical_contact_fax',
        'description': 'Technical Contact Fax Number',
    },
    'tech_fax_ext': {
        'field': 'technical_contact_fax_external',
        'description': 'Technical Contact Fax Number External',
    },
    'tech_name': {
        'field': 'technical_contact',
        'description': 'Technical Contact',
    },
    'tech_phone': {
        'field': 'technical_contact_phone',
        'description': 'Technical Contact Phone Number',
    },
    'tech_phone_ext': {
        'field': 'technical_contact_phone_external',
        'description': 'Technical Contact Phone Number External',
    },
    'tech_organization': {
        'field': 'technical_organization',
        'description': 'Technical Contact Organization',
    },
    'tech_postal_code': {
        'field': 'technical_address_postal_code',
        'description': 'Technical Contact Postal Code',
    },
    'tech_street': {
        'field': 'technical_address_street_address',
        'description': 'Technical Contact Street Address',
    },
    'url_of_the_icann_whois_inaccuracy_complaint_form': {
        'field': 'icann_whois_incuraccy_complaint_form_url',
        'description': 'URL of ICANN whois inaccuray complaint form',
    },
    'url_of_the_icann_whois_data_problem_reporting_system': {
        'field': 'icann_whois_data_problem_reporting_system_url',
        'description': 'URL of ICANN whois data problem reporting system',
    },
    'zone_c': {
        'field': 'zone_contact',
        'description': 'DNS Zone Contact',
    },
}
