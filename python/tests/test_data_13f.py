# pylint: disable=redefined-outer-name
"""This file contains tests for data_13f"""
from xml.etree import ElementTree
from edgar_filing_searcher.parsers.crawler_current_events import get_text
from edgar_filing_searcher.models import Data13f
import pytest