#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Utility methods for netlookup unit tests
"""
from typing import Union

from dns.flags import Flag
from dns.message import QueryMessage
from dns.name import Name
from dns.rdata import from_text
from dns.rdataclass import RdataClass
from dns.rdatatype import RdataType
from dns.rdtypes import ANY
from dns.resolver import Answer
from dns.rrset import RRset

from netlookup.network import Network


def validate_network_compare_methods(network: Network) -> None:
    """
    Validate a network object's compare methods
    """
    host = network.first_host
    if host is not None:
        assert network != str(host)
        assert network != host
        assert network < str(host)
        assert network < host
        assert network <= str(host)
        assert network <= host
        assert str(host) > network
        assert host > network
        assert str(host) >= network
        assert host >= network

    try:
        next_network = network.next()  # noqa
        assert next_network > network
        assert next_network >= network
    except IndexError:
        # Past network range max, this is ok
        pass


def validate_network(network: Network) -> None:
    """
    Validate a network object
    """
    assert isinstance(network, Network)
    assert isinstance(network.__repr__(), str)


def create_dns_txt_query_response(qname: str, record: Union[str, tuple]) -> Answer:
    """
    Create a DNS resolver answer for a valid TXT record for unit tests
    """
    qname = Name(qname.split('.'))
    if isinstance(record, tuple):
        record = ' '.join(record)

    # Common base rrset to work on, set as question to query
    rrset = RRset(name=qname, rdclass=RdataClass.IN, rdtype=RdataType.TXT)

    # Mock answer to query
    answer_rrset = rrset.copy()
    answer_rrset.add(from_text(rdclass=RdataClass.IN, rdtype=RdataType.TXT, tok=record))

    # Actual rrset returned and read by netlookup code
    result_rrset = rrset.copy()
    result_rrset.add(
        ANY.TXT.TXT(
            rdclass=RdataClass.IN,
            rdtype=RdataType.TXT,
            strings=bytes(record, encoding='utf-8')
        )
    )

    # Generate a semi-valid response. It may be not all fields are not filled correctly
    message = QueryMessage()
    message.flags = Flag.QR | Flag.RD | Flag.RA
    message.question.append(rrset)
    message.answer.append(answer_rrset)

    # Create answer with the response and the rrset we eventually want to return
    answer = Answer(qname=qname, rdtype=RdataType.TXT, rdclass=RdataClass.IN, response=message)
    answer.rrset = result_rrset

    return answer
