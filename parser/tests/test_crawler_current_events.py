# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=import-error
"""This file contains tests for crawler_current_events"""
import pytest
from crawler_current_events import parse_13f_filing_detail_urls, parse_sec_accession_no

from crawler_current_events import parse_infotable_xml_url, parse_primary_doc_xml_url, \
    parse_primary_doc_xml_and_infotable_xml_urls


@pytest.fixture
def xml_list():
    return ['/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml',
     '/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml']


@pytest.fixture
def current_events_text():
    my_file = open("fixtures/edgar_current_events.html", "rt")
    return my_file.read()


def test_parse_13f_filing_detail_urls(current_events_text):
    assert parse_13f_filing_detail_urls(current_events_text) == [
        'https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
        'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']


@pytest.fixture
def filing_detail_text():
    my_file = open("fixtures/EDGAR_Filing_Documents_for_0000909012-21-000060.html", "rt")
    return my_file.read()


def test_parse_sec_accession_no(filing_detail_text):
    assert parse_sec_accession_no(filing_detail_text) == '0000909012-21-000060'


def test_parse_primary_doc_xml_and_infotable_xml_urls(filing_detail_text):
    assert parse_primary_doc_xml_and_infotable_xml_urls(filing_detail_text) == \
           ['/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml',
 '/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml']


def test_parse_primary_doc_xml_url(xml_list):
    assert parse_primary_doc_xml_url(xml_list) == \
           'https://www.sec.gov/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml'


def test_parse_infotable_xml_url(xml_list):
    assert parse_infotable_xml_url(xml_list) == \
           'https://www.sec.gov/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml'
