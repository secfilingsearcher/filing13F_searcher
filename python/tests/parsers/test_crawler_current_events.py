# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
from datetime import date

import pytest

from edgar_filing_searcher.parsers.crawler_current_events import ensure_13f_filing_detail_urls, \
    get_subdirectories_for_specific_date, generate_dates

DATE_1 = date(2021, 1, 8)
DATE_2 = date(2021, 1, 9)
DATE_3 = date(2021, 1, 10)


@pytest.fixture
def subdirectories():
    """Creates an fixture with test_edgar_current_events.html data"""
    return ['1478997/0001478997-21-000001',
            '819864/0000819864-21-000002',
            '1567784/0000909012-21-000002',
            '1479844/0001479844-21-000001']


def test_get_subdirectories_for_specific_date():
    """Tests for get_subdirectories_for_specific_date"""
    actual = get_subdirectories_for_specific_date(DATE_1)
    assert actual == ['1478997/0001478997-21-000001',
                      '819864/0000819864-21-000002',
                      '1567784/0000909012-21-000002',
                      '1479844/0001479844-21-000001',
                      '1362987/0001362987-21-000001',
                      '1542265/0001542265-21-000001',
                      '740272/0000740272-21-000002',
                      '1799284/0001799284-21-000001',
                      '1800336/0001800336-21-000001',
                      '1744348/0001754960-21-000002',
                      '1664017/0001664017-21-000001',
                      '1370102/0001370102-21-000003',
                      '1766067/0001214659-21-000321',
                      '1008937/0001008937-21-000001',
                      '1761450/0001761450-21-000004',
                      '1015308/0001015308-21-000002',
                      '1387399/0001567619-21-000762']


def test_ensure_13f_filing_detail_urls(subdirectories):
    """Test for ensure_13f_filing_detail_urls"""

    actual = ensure_13f_filing_detail_urls(subdirectories)

    assert actual == \
           ['https://www.sec.gov/Archives/edgar/data/1478997/0001478997-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/819864/0000819864-21-000002-index.html',
            'https://www.sec.gov/Archives/edgar/data/1567784/0000909012-21-000002-index.html',
            'https://www.sec.gov/Archives/edgar/data/1479844/0001479844-21-000001-index.html']


def test_generate_dates():
    """Test for generate_dates"""

    actual = tuple(generate_dates(DATE_1, DATE_3))

    assert actual == (DATE_1, DATE_2, DATE_3)
