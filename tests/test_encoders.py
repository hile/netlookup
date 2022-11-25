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
