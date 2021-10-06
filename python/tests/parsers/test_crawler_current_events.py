# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
import pytest

from edgar_filing_searcher.parsers.crawler_current_events import ensure_13f_filing_detail_urls, \
    parse_13f_filing_detail_urls
from edgar_filing_searcher.errors import NoUrlException


@pytest.fixture
def edgar_current_events_text():
    """Creates an fixture with test_edgar_current_events.html data"""
    with open("tests/fixtures/edgar_current_events.html", "rt") as file:
        return file.read()


def test_parse_13f_filing_detail_urls(edgar_current_events_text):
    """Tests """

    actual = ensure_13f_filing_detail_urls(edgar_current_events_text)

    assert actual == \
           ['https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
            'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']


def test_parse_13f_filing_detail_urls_invalidText_raiseException():
    """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
    with pytest.raises(NoUrlException):
        parse_13f_filing_detail_urls("")


def test_get_subdirectories_for_specific_date():
    """Tests """
    pass


def test_ensure_13f_filing_detail_urls(edgar_current_events_text):
    """Tests ensure_13f_filing_detail_urls"""

    actual = ensure_13f_filing_detail_urls(edgar_current_events_text)

    assert actual == \
           ['https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
            'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']


def test_generate_dates():
    """Tests """
    pass
