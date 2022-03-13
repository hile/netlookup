
import re

from dns import resolver

RE_INCLUDE = re.compile(r'^include:(?P<rr>.*)$')
RE_IPV4 = re.compile(r'^ip4:(?P<prefix>.*)$')
RE_IPV6 = re.compile(r'^ip6:(?P<prefix>.*)$')


def google_rr_dns_query(record):
    """
    DNS query to get TXT record list of google networks
    """
    try:
        res = resolver.resolve(record, 'TXT')
        return str(res.rrset[0].strings[0], 'utf-8')
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        return None


def process_google_rr_ranges(record, loader_class):
    """
    Process RR records from google DNS query response
    """
    networks = []
    includes = []

    for field in google_rr_dns_query(record).split(' '):
        match = RE_IPV4.match(field)
        if match:
            networks.append(loader_class(match.groupdict()['prefix']))
            continue

        match = RE_IPV6.match(field)
        if match:
            networks.append(loader_class(match.groupdict()['prefix']))
            continue

        match = RE_INCLUDE.match(field)
        if match:
            include = match.groupdict()['rr']
            networks.extend(
                process_google_rr_ranges(include, loader_class)
            )
            includes.append(include)
            continue

    return networks
