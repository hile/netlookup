#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.encoders module
"""
import json

from netlookup.encoders import NetworkDataEncoder


def test_encoders_output(network_encoder_output):
    """
    Test
    """
    value = network_encoder_output[0]
    output = network_encoder_output[1]
    assert json.dumps(value, cls=NetworkDataEncoder) == output
