# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
"""docstring"""
import pytest
from crawler_current_events import get_13f_filing_detail_urls


@pytest.fixture
def current_events_text():
    myfile = open("fixtures/edgar_current_events.html", "rt")
    return myfile.read()


@pytest.fixture
def filing_detail_text():
    myfile = open("fixtures/edgar_current_events.html", "rt")
    return myfile.read()


def test_get_13f_filing_detail_urls(current_events_text):
    assert get_13f_filing_detail_urls(current_events_text) == [
        'https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
        'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']


def get_sec_accession_no(filing_detail_text):
    pass
