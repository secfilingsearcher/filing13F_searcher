# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=import-error
"""This file contains tests for crawler_current_events"""
import pytest
from crawler_current_events import get_13f_filing_detail_urls, get_sec_accession_no


@pytest.fixture
def current_events_text():
    my_file = open("fixtures/edgar_current_events.html", "rt")
    return my_file.read()


@pytest.fixture
def filing_detail_text():
    my_file = open("fixtures/EDGAR_Filing_Documents_for_0000909012-21-000060.html", "rt")
    return my_file.read()


def test_get_13f_filing_detail_urls(current_events_text):
    assert get_13f_filing_detail_urls(current_events_text) == [
        'https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
        'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']


def test_get_sec_accession_no(filing_detail_text):
    assert get_sec_accession_no(filing_detail_text) == []
