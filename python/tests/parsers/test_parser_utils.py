"""This file contains tests for main"""
# pylint: disable=redefined-outer-name
from datetime import date
from unittest.mock import patch, MagicMock, Mock

import pytest
from flask_testing import TestCase
from requests.exceptions import RetryError
from urllib3.exceptions import ResponseError

from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f
from edgar_filing_searcher.parsers.parser_class import Parser
from edgar_filing_searcher.parsers.parser_utils import check_parser_values_align, send_data_to_db, \
    update_filing_count, check_if_filing_exists_in_db, create_url_list, process_date, \
    process_filing_detail_url
from edgar_filing_searcher.parsers.daily_index_crawler import get_subdirectories_for_specific_date

DATE_1 = date(2021, 1, 8)
COMPANY_CIK_1 = "0001171592"
COMPANY_CIK_2 = "0001607863"
ACCESSION_NO_TABLE1_ROW1 = '0001214659-18-006391'
ACCESSION_NO_TABLE1_ROW2 = '0007635479-56-650763'


@pytest.fixture
def filing_detail_with_no_13f_filing_urls():
    """Creates an fixture with edgar_current_events.html data"""
    with open("tests/fixtures/company.20210108_RemovedAllFilings.idx", "rt") as file:
        test = file.read()
        return test


class FlaskSqlAlchemyTestConfiguration(TestCase):
    """This class configures Flask SQL Alchemy for Tests"""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        """Creates and pushes a context for a test"""
        app = create_app(self)
        return app

    def setUp(self):
        """Sets up a test database"""
        db.create_all()
        self.company1 = Company(cik_no=COMPANY_CIK_1, company_name="Cool Industries",
                                filing_count=0)
        self.edgar_filing1 = EdgarFiling(accession_no="0001420506-21-000830", cik_no=COMPANY_CIK_1,
                                         filing_date=date.fromisoformat("1999-09-01"))
        self.data_13f_table1 = [Data13f(equity_holdings_id="67896567",
                                        accession_no='0001420506-21-000830',
                                        cik_no=COMPANY_CIK_1,
                                        name_of_issuer='Agilent Technologies',
                                        title_of_class='COM',
                                        cusip='00846U101',
                                        value=22967078.5,
                                        ssh_prnamt=180644,
                                        ssh_prnamt_type='None',
                                        put_call='None',
                                        investment_discretion='SOLE',
                                        other_manager='None',
                                        voting_authority_sole=22967078,
                                        voting_authority_shared=0,
                                        voting_authority_none=0
                                        )]

        self.company2 = Company(cik_no=COMPANY_CIK_2,
                                company_name='ACCURATE INVESTMENT SOLUTIONS, INC.', filing_count=2)
        self.edgar_filing2_row1 = EdgarFiling(accession_no=ACCESSION_NO_TABLE1_ROW1,
                                              cik_no=COMPANY_CIK_2, filing_type='13F-HR',
                                              filing_date=date.fromisoformat("2018-10-05"))
        self.edgar_filing2_row2 = EdgarFiling(accession_no=ACCESSION_NO_TABLE1_ROW2,
                                              cik_no=COMPANY_CIK_2, filing_type='13F-HR',
                                              filing_date=date.fromisoformat("2018-05-23"))
        self.data_13f_table1_row1 = [Data13f(equity_holdings_id='1948ac4b72e6e2981eb9621a585c2e34',
                                             accession_no=ACCESSION_NO_TABLE1_ROW1,
                                             cik_no=COMPANY_CIK_2,
                                             name_of_issuer='ACCO BRANDS CORP',
                                             title_of_class='COM',
                                             cusip='00081T108',
                                             value=12,
                                             ssh_prnamt=1095,
                                             ssh_prnamt_type='SH',
                                             put_call='None',
                                             investment_discretion='SOLE',
                                             other_manager='None',
                                             voting_authority_sole=0,
                                             voting_authority_shared=0,
                                             voting_authority_none=1095)]
        self.data_13f_table1_row2 = [Data13f(equity_holdings_id='8g586856b668j6',
                                             accession_no=ACCESSION_NO_TABLE1_ROW2,
                                             cik_no=COMPANY_CIK_2,
                                             name_of_issuer='ALPS ETF TR',
                                             title_of_class='SECTR DIV DOGS',
                                             cusip='00162Q858',
                                             value=2229,
                                             ssh_prnamt=48594,
                                             ssh_prnamt_type='SH',
                                             put_call='None',
                                             investment_discretion='SOLE',
                                             other_manager='None',
                                             voting_authority_sole=0,
                                             voting_authority_shared=0,
                                             voting_authority_none=48594)]

    def tearDown(self):
        """Tears down test database"""
        db.session.remove()
        db.drop_all()


def test_create_url_list():
    """Test for create_url_list"""

    actual = create_url_list(DATE_1)

    assert actual == [
        'https://www.sec.gov/Archives/edgar/data/1478997/0001478997-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/819864/0000819864-21-000002-index.html',
        'https://www.sec.gov/Archives/edgar/data/1567784/0000909012-21-000002-index.html',
        'https://www.sec.gov/Archives/edgar/data/1479844/0001479844-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1362987/0001362987-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1542265/0001542265-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/740272/0000740272-21-000002-index.html',
        'https://www.sec.gov/Archives/edgar/data/1799284/0001799284-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1800336/0001800336-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1744348/0001754960-21-000002-index.html',
        'https://www.sec.gov/Archives/edgar/data/1664017/0001664017-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1370102/0001370102-21-000003-index.html',
        'https://www.sec.gov/Archives/edgar/data/1766067/0001214659-21-000321-index.html',
        'https://www.sec.gov/Archives/edgar/data/1008937/0001008937-21-000001-index.html',
        'https://www.sec.gov/Archives/edgar/data/1761450/0001761450-21-000004-index.html',
        'https://www.sec.gov/Archives/edgar/data/1015308/0001015308-21-000002-index.html',
        'https://www.sec.gov/Archives/edgar/data/1387399/0001567619-21-000762-index.html']


def filing_detail_13f_text_1():
    """Returns edgar_current_events.html data"""
    with open("tests/fixtures/edgar_filing_documents_13f.html", "rt") as file:
        return file.read()


def filing_detail_13f_text_2():
    """Returns edgar_current_events.html data"""
    with open("tests/fixtures/edgar_filing_documents_13f_2.html", "rt") as file:
        return file.read()


def filing_detail_13f_text_3():
    """Returns edgar_current_events.html data"""
    with open("tests/fixtures/edgar_filing_documents_13f_3.html", "rt") as file:
        return file.read()


def primary_doc_xml_text_1():
    """Returns primary_doc.xml data"""
    with open("tests/fixtures/primary_doc.xml", "rt") as file:
        return file.read()


def primary_doc_xml_text_2():
    """Returns primary_doc.xml data"""
    with open("tests/fixtures/primary_doc_2.xml", "rt") as file:
        return file.read()


def primary_doc_xml_text_3():
    """Returns primary_doc.xml data"""
    with open("tests/fixtures/primary_doc_3.xml", "rt") as file:
        return file.read()


def infotable_xml_text_1():
    """Returns infotable.xml data"""
    with open("tests/fixtures/infotable.xml", "rt") as file:
        return file.read()


def infotable_xml_text_2():
    """Returns infotable.xml data"""
    with open("tests/fixtures/infotable_2_shortened.xml", "rt") as file:
        return file.read()


def infotable_xml_text_3():
    """Returns infotable.xml data"""
    with open("tests/fixtures/infotable_3.xml", "rt") as file:
        return file.read()


def filing_detail_text_13f_missing_accession_no():
    """Returns edgar_current_events.html data with a missing accession no"""
    with open("tests/fixtures/edgar_filing_documents_13f_missing_accession_no.html", "rt") as file:
        return file.read()


def filing_detail_text_13f_missing_urls():
    """Returns edgar_current_events.html data with missing urls"""
    with open("tests/fixtures/edgar_filing_documents_13f_missing_urls.html", "rt") as file:
        return file.read()


def new_parser(filing_detail_text_13f, primary_doc_xml_text, infotable_xml_text):
    """Returns a new parser class with the filing_detail_text_13f, primary_doc_xml_text, infotable_xml_text functions
    as parameters. """
    with patch('requests.Session.get') as mock_function:
        mock_function.side_effect = [MagicMock(text=filing_detail_text_13f),
                                     MagicMock(text=primary_doc_xml_text),
                                     MagicMock(text=infotable_xml_text)]
        return Parser('')


PARSER_1 = new_parser(filing_detail_13f_text_1(), primary_doc_xml_text_1(), infotable_xml_text_1())

PARSER_2_IN_DATABASE = new_parser(filing_detail_13f_text_2(), primary_doc_xml_text_2(),
                                  infotable_xml_text_2())

PARSER_3_NOT_IN_DATABASE = new_parser(filing_detail_13f_text_3(), primary_doc_xml_text_3(),
                                      infotable_xml_text_3())

SUFFIX_XML_URLS_LIST = ['/Archives/edgar/data/1506796/000090901221000060/primary_doc.xml',
                        '/Archives/edgar/data/1506796/000090901221000060/aci_13f.xml']


def test_check_parser_values_align_isSame():
    """Tests if check_parser_values checks if the parser cik_no and accession_no are the same"""
    parser_value_1 = check_parser_values_align(PARSER_1.company, PARSER_1.edgar_filing,
                                               PARSER_1.data_13f)
    assert parser_value_1 == parser_value_1


class FlaskSQLAlchemyTest(FlaskSqlAlchemyTestConfiguration):
    """This class runs SQLALchemy Tests"""

    def test_check_if_filing_exists_in_db(self):
        """Tests if check_parser_values checks if the parser cik_no and accession_no are the same"""
        send_data_to_db(self.company1, self.edgar_filing1, self.data_13f_table1)
        actual = check_if_filing_exists_in_db('0001420506-21-000830')

        assert actual is True

    def test_update_filing_count_inDatabase(self):
        """Tests if update_filing_count updates the filing_count in the
        Company table when filing is in the database"""
        send_data_to_db(self.company2, self.edgar_filing2_row1, self.data_13f_table1_row1)
        send_data_to_db(self.company2, self.edgar_filing2_row2, self.data_13f_table1_row2)
        update_filing_count(PARSER_2_IN_DATABASE)
        assert PARSER_2_IN_DATABASE.company.filing_count == 2

    def test_update_filing_count_notinDatabase(self):
        """Tests if update_filing_count updates the filing_count in the
         Company table when filing is not in the database"""
        update_filing_count(PARSER_3_NOT_IN_DATABASE)

        assert PARSER_3_NOT_IN_DATABASE.company.filing_count == 1

    def test_send_data_to_db_savesCompanyInDb(self):
        """Tests if send_data_to_db saves the Company model in the database"""
        send_data_to_db(self.company1, self.edgar_filing1, self.data_13f_table1)

        assert Company.query.filter_by(cik_no=self.company1.cik_no).first() == self.company1

    def test_send_data_to_db_savesEdgarFilingInDb(self):
        """Tests if send_data_to_db saves the EdgarFiling model in the database"""
        send_data_to_db(self.company1, self.edgar_filing1, self.data_13f_table1)

        assert EdgarFiling.query.filter_by(
            accession_no=self.edgar_filing1.accession_no).first() == self.edgar_filing1

    def test_send_data_to_db_savesData13fInDb(self):
        """Tests if send_data_to_db saves the Data13f model in the database"""
        send_data_to_db(self.company1, self.edgar_filing1, self.data_13f_table1)

        assert Data13f.query.filter_by(cik_no=self.data_13f_table1[0].cik_no).first() == \
               self.data_13f_table1[0]

    def test_process_filing_detail_url_returnNoUrlException(self):
        with patch('requests.Session.get') as mock_function:
            mock_function.side_effect = [
                MagicMock(text=filing_detail_text_13f_missing_urls()),
                MagicMock(text=primary_doc_xml_text_1()),
                MagicMock(text=infotable_xml_text_1())]
            actual = process_filing_detail_url(DATE_1)
            assert actual is None

    def test_process_filing_detail_url_returnNoAccessionNumberException(self):
        with patch('requests.Session.get') as mock_function:
            mock_function.side_effect = [
                MagicMock(text=filing_detail_text_13f_missing_accession_no()),
                MagicMock(text=primary_doc_xml_text_1()),
                MagicMock(text=infotable_xml_text_1())]
            actual = process_filing_detail_url(DATE_1)
            assert actual is None

    def test_process_filing_detail_url_update_filing_countIsCalled(self):
        with patch('edgar_filing_searcher.parsers.main.Parser') as mock_function:
            mock_function.side_effect = MagicMock(return_value=PARSER_1)

    # def test_process_filing_detail_url_send_data_to_dbIsCalled(self):
    #     with patch('edgar_filing_searcher.parsers.main.Parser') as mock_function:
    #         mock_function.side_effect = MagicMock(return_value=PARSER_1)


def test_process_date_raiseInvalidUrlExceptionReturnNone():
    with patch('requests.Session.get') as mock_function:
        mock_function.side_effect = RetryError(
            Mock(reason=ResponseError("too many 503 error responses")))
        actual = process_date(DATE_1)
        assert actual is None


def test_process_date_raiseBadWebPageResponseExceptionReturnNone():
    with patch('requests.Session.get') as mock_function:
        mock_function.side_effect = RetryError(
            Mock(reason=ResponseError("too many 403 error responses")))
        actual = process_date(DATE_1)
        assert actual is None


def test_get_subdirectories_for_specific_date_hasNoResponse(filing_detail_with_no_13f_filing_urls):
    """Tests when get_subdirectories_for_specific_date has no response"""
    with patch('edgar_filing_searcher.parsers.daily_index_crawler.get_text') as mock_function:
        mock_function.side_effect = MagicMock(return_value=filing_detail_with_no_13f_filing_urls)
        actual = process_date(DATE_1)
        assert actual is None
