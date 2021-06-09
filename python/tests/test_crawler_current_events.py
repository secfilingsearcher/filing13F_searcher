# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
from edgar_filing_searcher.parsers.crawler_current_events import parse_13f_filing_detail_urls, \
    parse_sec_accession_no, parse_infotable_xml_url, parse_primary_doc_xml_url, \
    parse_primary_doc_xml_and_infotable_xml_urls
import pytest


@pytest.fixture
def current_events_text():
    """This function creates an fixture with test edgar_current_events html data"""
    with open("tests/fixtures/edgar_current_events.html", "rt") as file:
        return file.read()


@pytest.fixture
def filing_detail_text():
    """This function creates an fixture with test EDGAR filing document html data"""
    with open("tests/fixtures/edgar_filing_documents_for_0001852858-21-000001.html", "r") as file:
        return file.read()


@pytest.fixture
def xml_list():
    """This function creates an fixture with test primary_doc.xml data"""
    return ['/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml',
     '/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml']


def test_parse_13f_filing_detail_urls(current_events_text):
    """This function tests test_parse_13f_filing_detail_urls"""
    assert parse_13f_filing_detail_urls(current_events_text) == [
        'https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
        'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']


def test_parse_sec_accession_no(filing_detail_text):
    """This function tests parse_sec_accession_no"""
    assert parse_sec_accession_no(filing_detail_text) == '0001852858-21-000001'


def test_parse_primary_doc_xml_and_infotable_xml_urls(filing_detail_text):
    """This function tests parse_primary_doc_xml_and_infotable_xml_urls"""
    assert parse_primary_doc_xml_and_infotable_xml_urls(filing_detail_text) == \
           ['/Archives/edgar/data/1852858/000185285821000001/primary_doc.xml',
            '/Archives/edgar/data/1852858/000185285821000001/infotable.xml']


def test_parse_primary_doc_xml_url(xml_list):
    """This function tests parse_primary_doc_xml_url"""
    assert parse_primary_doc_xml_url(xml_list) == \
           'https://www.sec.gov/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml'


def test_parse_infotable_xml_url(xml_list):
    """This function tests parse_infotable_xml_url"""
    assert parse_infotable_xml_url(xml_list) == \
           'https://www.sec.gov/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml'
