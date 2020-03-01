
from systematic_networks.network_sets.utils import google_rr_dns_query
from systematic_networks.network_sets.gcp import ADDRESS_LIST_RECORD as GCP_TXT_RECORD
from systematic_networks.network_sets.google import ADDRESS_LIST_RECORD as GOOGLE_TXT_RECORD

INVALID_QUERY = '_invalid.example.com'
NO_TXT_QUERY = 'git.tuohela.net'


def test_network_sets_dns_gcp_rrset_query():
    """
    Test resolving GCP records
    """
    record = google_rr_dns_query(GCP_TXT_RECORD)
    assert isinstance(record, str)


def test_network_sets_dns_google_rrset_query():
    """
    Test resolving Google Service SPF records
    """
    record = google_rr_dns_query(GOOGLE_TXT_RECORD)
    assert isinstance(record, str)


def test_network_sets_dns_invalid_query():
    """
    Test resolving invalid TXT records
    """
    assert google_rr_dns_query(INVALID_QUERY) is None


def test_network_sets_dns_no_txt_record_query():
    """
    Test resolving invalid TXT records
    """
    assert google_rr_dns_query(NO_TXT_QUERY) is None
