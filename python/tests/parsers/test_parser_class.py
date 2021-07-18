# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
from unittest.mock import patch, MagicMock

import pytest

from edgar_filing_searcher.parsers.errors import CantFindUrlException
from edgar_filing_searcher.parsers.parser_class import Parser


@pytest.fixture
def filing_detail_text_13f():
    """This function creates an fixture with test edgar_current_events html data"""
    with open("tests/fixtures/edgar_filing_documents_13f.html", "rt") as file:
        return file.read()


@pytest.fixture
def primary_doc_xml_text():
    """This function creates an fixture with test edgar_current_events html data"""
    with open("tests/fixtures/primary_doc.xml", "rt") as file:
        return file.read()


@pytest.fixture
def infotable_xml_text():
    """This function creates an fixture with test edgar_current_events html data"""
    with open("tests/fixtures/infotable.xml", "rt") as file:
        return file.read()


@pytest.fixture
def parser(filing_detail_text_13f, primary_doc_xml_text, infotable_xml_text):
    with patch('requests.get') as mock_function:
        mock_function.side_effect = [MagicMock(text=filing_detail_text_13f), MagicMock(text=primary_doc_xml_text),
                                     MagicMock(text=infotable_xml_text)]
        return Parser('')


SUFFIX_XML_URLS_LIST = ['/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml',
                        '/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml']


def test_parse_sec_accession_no(filing_detail_text_13f, parser):
    """This function tests parse_sec_accession_no"""

    actual = parser.parse_sec_accession_no(filing_detail_text_13f)

    assert actual == '0001852858-21-000001'


def test_parse_primary_doc_xml_and_infotable_xml_urls(filing_detail_text_13f, parser):
    """This function tests parse_primary_doc_xml_and_infotable_xml_urls"""

    actual = parser.parse_primary_doc_xml_and_infotable_xml_urls(filing_detail_text_13f)

    assert actual == \
           ['/Archives/edgar/data/1852858/000185285821000001/primary_doc.xml',
            '/Archives/edgar/data/1852858/000185285821000001/infotable.xml']


def test_ensure_primary_doc_xml_url(parser):
    """This function tests parse_primary_doc_xml_url"""

    actual = parser.ensure_primary_doc_xml_url(SUFFIX_XML_URLS_LIST)

    assert actual == 'https://www.sec.gov/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml'


def test_ensure_primary_doc_xml_url_invalidText_raiseException(parser):
    """This function tests parse_primary_doc_xml_url"""
    with pytest.raises(CantFindUrlException):
        parser.ensure_primary_doc_xml_url("")


def test_ensure_infotable_xml_url(parser):
    """This function tests parse_infotable_xml_url"""

    actual = parser.ensure_infotable_xml_url(SUFFIX_XML_URLS_LIST)

    assert actual == 'https://www.sec.gov/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml'


def test_ensure_infotable_xml_url_invalidText_raiseException(parser):
    """This function tests parse_infotable_xml_url"""
    with pytest.raises(CantFindUrlException):
        parser.ensure_infotable_xml_url("")
