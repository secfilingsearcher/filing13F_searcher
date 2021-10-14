# pylint: disable=redefined-outer-name
"""This file contains tests for daily_index_crawler"""
from _elementtree import ParseError
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest

from edgar_filing_searcher.models import EdgarFiling, Company, Data13f
from edgar_filing_searcher.errors import NoUrlException, NoAccessionNumberException
from edgar_filing_searcher.parsers.parser_class import Parser


def filing_detail_text_13f():
    """Returns edgar_current_events.html data"""
    with open("tests/fixtures/edgar_filing_documents_13f.html", "rt") as file:
        return file.read()


def filing_detail_text_13f_missing_urls():
    """Returns edgar_current_events.html data with missing urls"""
    with open("tests/fixtures/edgar_filing_documents_13f_missing_urls.html", "rt") as file:
        return file.read()


def filing_detail_text_13f_missing_accession_no():
    """Returns edgar_current_events.html data with a missing accession no"""
    with open("tests/fixtures/edgar_filing_documents_13f_missing_accession_no.html", "rt") as file:
        return file.read()


def primary_doc_xml_text():
    """Returns primary_doc.xml data"""
    with open("tests/fixtures/primary_doc.xml", "rt") as file:
        return file.read()


def infotable_xml_text():
    """Returns infotable.xml data"""
    with open("tests/fixtures/infotable.xml", "rt") as file:
        return file.read()


def new_parser(filing_detail_text_13f, primary_doc_xml_text, infotable_xml_text):
    """Returns a new parser class with the filing_detail_text_13f, primary_doc_xml_text, infotable_xml_text functions 
    as parameters. """
    with patch('requests.Session.get') as mock_function:
        mock_function.side_effect = [MagicMock(text=filing_detail_text_13f),
                                     MagicMock(text=primary_doc_xml_text),
                                     MagicMock(text=infotable_xml_text)]
        return Parser('')


PARSER = new_parser(filing_detail_text_13f(), primary_doc_xml_text(), infotable_xml_text())

SUFFIX_XML_URLS_LIST = ['/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml',
                        '/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml']


def test_parser_setsCompany():
    """Tests if parser sets the Company field"""

    company = Company(cik_no="0001852858", company_name="Everhart Financial Group, Inc.", filing_count=0)

    assert PARSER.company == company


def test_parser_setsEdgarFiling():
    """Tests if parser sets the EdgarFiling field"""

    edgar_filing = EdgarFiling(accession_no="0001852858-21-000001",
                               cik_no="0001852858",
                               filing_type="13F-HR",
                               filing_date=datetime.strptime('03-26-2021', '%m-%d-%Y'))

    assert PARSER.edgar_filing == edgar_filing


def test_parser_setsData13f():
    """Tests if parser sets the Data13f field"""
    data_13f_table = [Data13f(equity_holdings_id='a72c809fdf734348a910bbb39d2c5ac4',
                              accession_no='0001852858-21-000001',
                              cik_no='0001852858',
                              name_of_issuer='ALTERYX INC',
                              title_of_class='COM CL A',
                              cusip='02156B103',
                              value=Decimal(353),
                              ssh_prnamt=2893,
                              ssh_prnamt_type='SH',
                              put_call=None,
                              investment_discretion='SOLE',
                              other_manager=None,
                              voting_authority_sole=0,
                              voting_authority_shared=0,
                              voting_authority_none=2893)
                      ]

    assert PARSER.data_13f == data_13f_table


def test_parser_AccessionNoInvalid_raisesNoAccessionNo():
    """Tests if parser raises the NoAccessionNo exception when the accession no is not found"""
    with pytest.raises(NoAccessionNumberException):
        new_parser(filing_detail_text_13f_missing_accession_no(), primary_doc_xml_text(), infotable_xml_text())


def test_parser_primaryDocXmlInvalid_raisesParseError():
    """Tests if parser raises the ParseError exception when the primary_doc.xml file is invalid"""
    invalid_xml = ""
    with pytest.raises(ParseError):
        new_parser(filing_detail_text_13f(), invalid_xml, infotable_xml_text())


def test_parser_XmlUrlInvalid_raisesUrlErrorException():
    """Tests if parser raises the UrlErrorException exception when the xml url is invalid"""
    with pytest.raises(NoUrlException):
        new_parser(filing_detail_text_13f_missing_urls(), primary_doc_xml_text(), infotable_xml_text())
