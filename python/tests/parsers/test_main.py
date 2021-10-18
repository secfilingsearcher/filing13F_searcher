"""This file contains tests for main_parser"""
import sys
from edgar_filing_searcher.parsers.main import my_handler, change_sys_excepthook


def test_my_handler(caplog):
    """Tests if my_handler handles exceptions in caplog.text"""
    try:
        1 / 0
    except ZeroDivisionError:
        my_handler(*sys.exc_info())
        assert "Uncaught exception" in caplog.text


def test_change_sys_excepthook():
    """Tests if change_sys_excepthook updates the sys_excepthook"""
    change_sys_excepthook()
    assert sys.excepthook is my_handler
    sys.excepthook = sys.__excepthook__
