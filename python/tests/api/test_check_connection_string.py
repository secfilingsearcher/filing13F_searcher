# pylint: disable=redefined-outer-name
"""This file contains tests for check connection string"""
import pytest

from api.check_connection_string import check_postgres_connection_string
from edgar_filing_searcher.parsers.errors import InvalidConnectionStringException

VALID_CONNECTION_STRING = "sqlite://"
INVALID_CONNECTION_STRING = ""


def test_check_postgres_connection_string_valid_connection_string_NoError():
    """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
    try:
        check_postgres_connection_string(VALID_CONNECTION_STRING)
    except:
        assert False


def test_check_postgres_connection_string_invalid_connection_string_raiseException():
    """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
    with pytest.raises(InvalidConnectionStringException):
        check_postgres_connection_string(INVALID_CONNECTION_STRING)
