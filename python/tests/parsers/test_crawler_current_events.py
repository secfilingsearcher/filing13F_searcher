# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
import pytest
from edgar_filing_searcher.parsers.crawler_current_events import parse_13f_filing_detail_urls


@pytest.fixture
def edgar_current_events_text():
    """This function creates an fixture with test_edgar_current_events.html data"""
    with open("tests/fixtures/edgar_current_events.html", "rt") as file:
        return file.read()


def test_parse_13f_filing_detail_urls(edgar_current_events_text):
    """This function tests parse_13f_filing_detail_urls"""

    actual = parse_13f_filing_detail_urls(edgar_current_events_text)

    assert actual == \
           ['https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
            'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']
