"""
Unit tests for netlookup.whois.groups module
"""

from netlookup.whois.groups import InformationSectionGroup

from .mock import get_empty_response, TEST_INETNUM_LINE


def test_whois_groups_empty_group_properties():
    """
    Test properties of empty InformationSectionGroup object
    """
    group = InformationSectionGroup(get_empty_response(), TEST_INETNUM_LINE)
    assert group.section == 'inetnum'
    assert group.is_empty is True
    assert group.to_dict() == {'inetnum': {}}
