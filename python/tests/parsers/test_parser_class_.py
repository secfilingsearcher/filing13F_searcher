# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
import pytest
from edgar_filing_searcher.parsers.parser_class import Parser
from unittest.mock import patch, MagicMock


@pytest.fixture
def filing_detail_text_13f():
    """This function creates an fixture with test EDGAR_filing_document.html data"""
    with open("tests/fixtures/edgar_filing_documents_for_0001852858-21-000001.html", "r") as file:
        return file.read()


@pytest.fixture
def edgar_current_events_text():
    """This function creates an fixture with test edgar_current_events html data"""
    with open("tests/fixtures/edgar_Filing_Documents_for_0001843111-21-000003.html", "rt") as file:
        return file.read()


@pytest.fixture
def parser(edgar_current_events_text):
    with patch('requests.get') as mock_function:
        mock_function.side_effect = [MagicMock(text=edgar_current_events_text), MagicMock(text=filing_detail_text_13f)]
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


def test_parse_primary_doc_xml_url(parser):
    """This function tests parse_primary_doc_xml_url"""

    actual = parser.parse_primary_doc_xml_url(SUFFIX_XML_URLS_LIST)

    assert actual == 'https://www.sec.gov/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml'


def test_parse_infotable_xml_url(parser):
    """This function tests parse_infotable_xml_url"""

    actual = parser.parse_infotable_xml_url(SUFFIX_XML_URLS_LIST)

    assert actual == 'https://www.sec.gov/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml'
