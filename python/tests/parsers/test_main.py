"""This file contains tests for main"""
# pylint: disable=redefined-outer-name
import sys
from datetime import date

import pytest
from flask_testing import TestCase

from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f
from edgar_filing_searcher.parsers.main import create_url_list, send_data_to_db, update_filing_counts, my_handler, \
    change_sys_excepthook

DATE_1 = date(2021, 1, 8)


@pytest.fixture
def edgar_current_events_text():
    """Creates an fixture with edgar_current_events.html data"""
    with open("tests/fixtures/edgar_current_events.html", "rt") as file:
        return file.read()


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
        self.company = Company(cik_no="0001171592", company_name="Cool Industries", filing_count=0)
        self.edgar_filing = EdgarFiling(accession_no="0001420506-21-000830", cik_no="0001171592",
                                        filing_date=date.fromisoformat("1999-09-01"))
        self.data_13f_table = [Data13f(equity_holdings_id="67896567",
                                       accession_no='0001420506-21-000830',
                                       cik_no='56464565767',
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

    def tearDown(self):
        """Tears down test database"""
        db.session.remove()
        db.drop_all()


def test_create_url_list():
    """Test for create_url_list"""

    actual = create_url_list(DATE_1)

    assert actual == ['https://www.sec.gov/Archives/edgar/data/1478997/0001478997-21-000001-index.html',
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


class FlaskSQLAlchemyTest(FlaskSqlAlchemyTestConfiguration):
    """This class runs SQLALchemy Tests"""

    def test_update_filing_counts(self):
        """Tests update_filing_counts"""
        cik_no = '0001171592'
        send_data_to_db(self.company, self.edgar_filing, self.data_13f_table)

        update_filing_counts([cik_no])

        assert Company.query.filter_by(cik_no=cik_no).first().filing_count == 1

    def test_send_data_to_db_savesCompanyInDb(self):
        """Tests if send_data_to_db saves the Company model in the database"""
        send_data_to_db(self.company, self.edgar_filing, self.data_13f_table)

        assert Company.query.filter_by(cik_no=self.company.cik_no).first() == self.company

    def test_send_data_to_db_savesEdgarFilingInDb(self):
        """Tests if send_data_to_db saves the EdgarFiling model in the database"""
        send_data_to_db(self.company, self.edgar_filing, self.data_13f_table)

        assert EdgarFiling.query.filter_by(accession_no=self.edgar_filing.accession_no).first() == self.edgar_filing

    def test_send_data_to_db_savesData13fInDb(self):
        """Tests if send_data_to_db saves the Data13f model in the database"""
        send_data_to_db(self.company, self.edgar_filing, self.data_13f_table)

        assert Data13f.query.filter_by(cik_no=self.data_13f_table[0].cik_no).first() == self.data_13f_table[0]


def test_change_sys_excepthook():
    change_sys_excepthook()
    assert sys.excepthook is my_handler
    sys.excepthook = sys.__excepthook__


def test_my_handler(caplog):
    try:
        1 / 0
    except ZeroDivisionError:
        my_handler(*sys.exc_info())
        assert "Uncaught exception" in caplog.text
