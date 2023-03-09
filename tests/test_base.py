#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for netlookup.base module
"""
import re

import pytest

from netlookup.base import match_patterns

RE_TEST_PATTERNS = (
    re.compile(r'^(?P<number>\d+) is a number string$'),

)


def test_base_match_patterns_match_found():
    """
    Test match_patterns function with found pattern matcn
    """
    match = match_patterns(RE_TEST_PATTERNS, '1234 is a number string')
    assert match == {'number': '1234'}


def test_base_match_patterns_no_match_found():
    """
    Test match_patterns function with found pattern matcn
    """
    with pytest.raises(ValueError):
        match_patterns(RE_TEST_PATTERNS, '1234 is not a match')
