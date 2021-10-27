# pylint: disable=redefined-outer-name
"""This file contains tests for daily_index_crawler"""
from datetime import date
import httpretty
import pytest
import requests
from unittest.mock import patch, MagicMock, Mock

from urllib3.exceptions import ResponseError

from edgar_filing_searcher.parsers.daily_index_crawler import ensure_13f_filing_detail_urls, \
    get_subdirectories_for_specific_date, generate_dates, get_request_response, get_quarter
from edgar_filing_searcher.errors import BadWebPageResponseException, InvalidUrlException

from requests.exceptions import RetryError

DATE_1 = date(2021, 1, 8)
DATE_2 = date(2021, 1, 9)
DATE_3 = date(2021, 1, 10)
SUBDIRECTORIES = ['1478997/0001478997-21-000001',
                  '819864/0000819864-21-000002',
                  '1567784/0000909012-21-000002',
                  '1479844/0001479844-21-000001']


@pytest.fixture
def filing_detail_with_no_13f_filing_urls():
    """Creates an fixture with edgar_current_events.html data"""
    with open("tests/fixtures/company.20210108_RemovedAllFilings.idx", "rt") as file:
        test = file.read()
        return test


@httpretty.activate(allow_net_connect=False)
def test_get_response_noError_StatusCode():
    """Tests get_response status code when there is no error"""
    test_url = "http://foo-api.com/data?page=2"
    httpretty.register_uri(
        httpretty.GET,
        test_url,
        body='{}',
        status=200,
        content_type="text/json",
    )
    actual = get_request_response(test_url)
    assert actual.status_code == 200


@httpretty.activate(allow_net_connect=False)
def test_get_response_noError_NumberOfRequests():
    """Tests get_response number of requests code when there is no error"""
    test_url = "http://foo-api.com/data?page=2"
    httpretty.register_uri(
        httpretty.GET,
        test_url,
        body='{}',
        status=200,
        content_type="text/json",
    )
    get_request_response(test_url)
    assert len(httpretty.latest_requests()) == 1


@httpretty.activate(allow_net_connect=False)
def test_get_response_statusError_StatusCode():
    """Tests get_response status code when there is an error"""
    test_url = "http://foo-api.com/data?page=2"
    httpretty.register_uri(
        httpretty.GET,
        test_url,
        body='{}',
        status=503,
        content_type="text/json",
    )

    try:
        get_request_response(test_url)
        assert False, "no error thrown"
    except requests.exceptions.RetryError:
        pass


@httpretty.activate(allow_net_connect=False)
def test_get_response_statusError_NumberOfRequests():
    """Tests get_response number of requests code when there is an error"""
    test_url = "http://foo-api.com/data?page=2"
    httpretty.register_uri(
        httpretty.GET,
        test_url,
        body='{}',
        status=503,
        content_type="text/json",
    )

    try:
        get_request_response(test_url)
    except requests.exceptions.RetryError:
        pass
    assert len(httpretty.latest_requests()) == 4


def test_get_quarter_first():
    """Tests the get_quarter function for the first quarter"""
    actual = get_quarter(date(2020, 2, 1))

    assert actual == 1


def test_get_quarter_second():
    """Tests the get_quarter function for the second quarter"""
    actual = get_quarter(date(2020, 5, 1))

    assert actual == 2


def test_get_quarter_third():
    """Tests the get_quarter function for the third quarter"""
    actual = get_quarter(date(2020, 8, 1))

    assert actual == 3


def test_get_quarter_fourth():
    """Tests the get_quarter function for the fourth quarter"""
    actual = get_quarter(date(2020, 11, 1))

    assert actual == 4


def test_get_subdirectories_for_specific_date_hasSubdirectories():
    """Tests when get_subdirectories_for_specific_date has subdirectories"""
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


def test_get_subdirectories_for_specific_date_hasInvalidURL():
    """Tests when get_subdirectories_for_specific_date has an invalid URL"""
    with pytest.raises(InvalidUrlException):
        get_subdirectories_for_specific_date(DATE_2)


def test_get_subdirectories_for_specific_date_hasBadWebPageResponse():
    """Tests when get_subdirectories_for_specific_date has no response"""
    with patch('requests.Session.get') as mock_function:
        mock_function.side_effect = RetryError(
            Mock(reason=ResponseError("too many 503 error responses")))
        with pytest.raises(BadWebPageResponseException):
            get_subdirectories_for_specific_date(DATE_2)


def test_get_subdirectories_for_specific_date_hasNoResponse(filing_detail_with_no_13f_filing_urls):
    """Tests when get_subdirectories_for_specific_date has no response"""
    with patch('edgar_filing_searcher.parsers.daily_index_crawler.get_text') as mock_function:
        mock_function.side_effect = MagicMock(return_value=filing_detail_with_no_13f_filing_urls)
        actual = get_subdirectories_for_specific_date(DATE_1)
        assert actual == []


def test_ensure_13f_filing_detail_urls():
    """Test for ensure_13f_filing_detail_urls"""
    actual = ensure_13f_filing_detail_urls(SUBDIRECTORIES)

    assert actual == \
           ['https://www.sec.gov/Archives/edgar/data/1478997/0001478997-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/819864/0000819864-21-000002-index.html',
            'https://www.sec.gov/Archives/edgar/data/1567784/0000909012-21-000002-index.html',
            'https://www.sec.gov/Archives/edgar/data/1479844/0001479844-21-000001-index.html']


def test_ensure_13f_filing_detail_urls_no():
    """Test for ensure_13f_filing_detail_urls"""
    actual = ensure_13f_filing_detail_urls([])

    assert actual == []


def test_generate_dates_differentDates():
    """Test when generate_dates has different dates"""
    actual = tuple(generate_dates(DATE_1, DATE_3))

    assert actual == (DATE_1, DATE_2, DATE_3)


def test_generate_dates_sameDates():
    """Test when generate_dates has the same dates"""
    actual = tuple(generate_dates(DATE_1, DATE_1))

    assert actual == (DATE_1,)
