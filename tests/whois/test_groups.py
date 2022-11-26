"""
Unit tests for netlookup.whois.groups module
"""

from netlookup.whois.groups import InformationSectionGroup

from .constants import MOCK_INETNUM_LINE


def test_whois_groups_empty_group_properties(empty_whois_response):
    """
    Test properties of empty InformationSectionGroup object
    """
    group = InformationSectionGroup(empty_whois_response, MOCK_INETNUM_LINE)
    assert group.section == 'inetnum'
    assert group.is_empty is True
    assert group.as_dict() == {'inetnum': {}}
