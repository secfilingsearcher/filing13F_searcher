"""This file contains tests for main"""
# pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest
from flask_testing import TestCase

from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f
from edgar_filing_searcher.parsers.main import create_url_list, send_data_to_db, update_filing_counts


@pytest.fixture
def current_events_text():
    """This function creates an fixture with test edgar_current_events html data"""
    with open("tests/fixtures/edgar_current_events.html", "rt") as file:
        return file.read()


class FlaskSqlAlchemyTestConfiguration(TestCase):
    """This class configures Flask SQL Alchemy Tests"""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        """This function creates and pushes a context for a test"""
        app = create_app(self)
        return app

    def setUp(self):
        """This function tests sets up test database"""
        db.create_all()
        self.company = Company(cik_no="0001171592", company_name="Cool Industries", filing_count=0)
        self.edgar_filing = EdgarFiling(accession_no="0001420506-21-000830", cik_no="0001171592",
                                        filing_date=datetime.fromisoformat("1999-09-01"))
        self.data_13f_table = Data13f(equity_holdings_id="67896567",
                                      accession_no='0001420506-21-000830',
                                      cik_no='56464565767',
                                      name_of_issuer='Agilent Technologies',
                                      title_of_class='COM',
                                      cusip='00846U101',
                                      value='22967078',
                                      ssh_prnamt='180644',
                                      ssh_prnamt_type='None',
                                      put_call='None',
                                      investment_discretion='SOLE',
                                      other_manager='None',
                                      voting_authority_sole='22967078',
                                      voting_authority_shared='0',
                                      voting_authority_none='0')
        db.session.merge(self.company)
        db.session.merge(self.edgar_filing)
        db.session.merge(self.data_13f_table)
        db.session.commit()

    def tearDown(self):
        """This function tests tears down test database"""
        db.session.remove()
        db.drop_all()


def test_create_url_list(current_events_text):
    """This function tests test_parse_13f_filing_detail_urls"""
    with patch('requests.get') as mock_function:
        mock_function.return_value = MagicMock(text=current_events_text)
        fake_url = ""

        actual = create_url_list(fake_url)

        assert actual == [
            'https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
            'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']


class FlaskSQLAlchemyTest(FlaskSqlAlchemyTestConfiguration):
    """This class runs SQL ALchemy Tests"""

    def test_update_filing_counts(self):
        """This function tests update_filing_counts"""
        cik_no = '0001171592'

        update_filing_counts([cik_no])

        assert Company.query.filter_by(cik_no=cik_no).first().filing_count == 1

    def test_send_data_to_db_savesCompanyInDb(self):
        """This function tests send_data_to_db_savesCompanyInDb"""
        self.company_2 = Company(cik_no="000984343", company_name="True Blue", filing_count=0)
        self.edgar_filing_2 = EdgarFiling(accession_no="0001420506", cik_no="000984343",
                                          filing_date=datetime.fromisoformat("2002-04-10"))
        self.data_13f_table_2 = [Data13f(equity_holdings_id="67896567",
                                         accession_no='0001420506',
                                         cik_no='00054654983',
                                         name_of_issuer='Agilent Technologies',
                                         title_of_class='COM',
                                         cusip='00846U101',
                                         value='22967078',
                                         ssh_prnamt='180644',
                                         ssh_prnamt_type='None',
                                         put_call='None',
                                         investment_discretion='SOLE',
                                         other_manager='None',
                                         voting_authority_sole='22967078',
                                         voting_authority_shared='0',
                                         voting_authority_none='0')]

        send_data_to_db(self.company_2, self.edgar_filing_2, self.data_13f_table_2)

        assert Company.query.filter_by(cik_no='000984343').first() == self.company_2

    def test_send_data_to_db_savesEdgarFilingInDb(self):
        """This function tests send_data_to_db_savesEdgarFilingInDb"""
        self.company_3 = Company(cik_no="8673434", company_name="Purple Company", filing_count=1)
        self.edgar_filing_3 = EdgarFiling(accession_no="3453456", cik_no="8673434",
                                          filing_date=datetime.fromisoformat("2000-06-11"))
        self.data_13f_table_3 = [Data13f(equity_holdings_id="67896567",
                                         accession_no='3453456',
                                         cik_no='654656465',
                                         name_of_issuer='Agilent Technologies',
                                         title_of_class='COM',
                                         cusip='00846U101',
                                         value='22967078',
                                         ssh_prnamt='180644',
                                         ssh_prnamt_type='None',
                                         put_call='None',
                                         investment_discretion='SOLE',
                                         other_manager='None',
                                         voting_authority_sole='22967078',
                                         voting_authority_shared='0',
                                         voting_authority_none='0')]

        send_data_to_db(self.company_3, self.edgar_filing_3, self.data_13f_table_3)

        assert EdgarFiling.query.filter_by(cik_no='8673434').first() == self.edgar_filing_3

    def test_send_data_to_db_savesData13fInDb(self):
        """This function tests send_data_to_db_savesData13fInDb"""
        self.company_4 = Company(cik_no="009039443", company_name="Apple Industries", filing_count=0)
        self.edgar_filing_4 = EdgarFiling(accession_no="78945835", cik_no="009039443",
                                          filing_date=datetime.fromisoformat("2000-06-11"))
        self.data_13f_table_4 = [Data13f(equity_holdings_id="67896567",
                                         accession_no='78945835',
                                         cik_no='009039443',
                                         name_of_issuer='Agilent Technologies',
                                         title_of_class='COM',
                                         cusip='00846U101',
                                         value='22967078',
                                         ssh_prnamt='180644',
                                         ssh_prnamt_type='None',
                                         put_call='None',
                                         investment_discretion='SOLE',
                                         other_manager='None',
                                         voting_authority_sole='22967078',
                                         voting_authority_shared='0',
                                         voting_authority_none='0')]

        send_data_to_db(self.company_4, self.edgar_filing_4, self.data_13f_table_4)

        assert Data13f.query.filter_by(cik_no='009039443').first() == self.data_13f_table_4[0]
