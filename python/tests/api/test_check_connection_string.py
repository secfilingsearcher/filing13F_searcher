# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
import os

import pytest

from edgar_filing_searcher.api.routes.check_connection_string import postgres_test

from edgar_filing_searcher.parsers.errors import InvalidConnectionStringException


def test_check_connection_string():
    """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
    os.environ["DB_CONNECTION_STRING"] = ""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    with pytest.raises(NoUrlException):
        parse_13f_filing_detail_urls("")


def test_check_connection_string_invalidConnectionString_raiseException():
    """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
    os.environ["DB_CONNECTION_STRING"] = ""
    with pytest.raises(InvalidConnectionStringException):
        postgres_test()
