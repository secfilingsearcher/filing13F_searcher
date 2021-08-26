# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
import os

import pytest

from edgar_filing_searcher.api.routes.check_connection_string import postgres_test

from edgar_filing_searcher.parsers.errors import InvalidConnectionStringException


def check_connection_string():
    pass


def test_check_connection_string():
    """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
    os.environ["DB_CONNECTION_STRING"] = "sqlite://"
    actual = check_connection_string()
    assert actual == \
           ['https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html']


def test_check_connection_string_invalidConnectionString_raiseException():
    """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
    os.environ["DB_CONNECTION_STRING"] = ""
    with pytest.raises(InvalidConnectionStringException):
        postgres_test()
