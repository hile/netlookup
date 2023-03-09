#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common functions for netlookup.network_sets unit tests
"""
from typing import Type

from netaddr.ip.sets import IPSet

from netlookup.network_sets.base import NetworkSet


def validate_network_set_properties(
        network_set: NetworkSet,
        network_set_class: Type) -> None:
    """
    Validate some of the common properties of network sets
    """
    assert isinstance(network_set, network_set_class)
    assert isinstance(network_set.ipset, IPSet)
