"""This file contains tests for main"""
# pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import patch, MagicMock
from flask_testing import TestCase
import pytest
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f
from edgar_filing_searcher.parsers.main import create_url_list, send_data_to_db, update_filing_count
from edgar_filing_searcher.database import db
from edgar_filing_searcher.api import create_app


@pytest.fixture
def current_events_text():
    """This function creates an fixture with test edgar_current_events html data"""
    with open("tests/fixtures/edgar_current_events.html", "rt") as file:
        return file.read()


def test_create_url_list(current_events_text):
    """This function tests test_parse_13f_filing_detail_urls"""
    with patch('requests.get') as mock_function:
        mock_function.return_value = MagicMock(text=current_events_text)
        fake_url = ""
        assert create_url_list(fake_url) == [
            'https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1852858/0001852858-21-000001-index.html',
            'https://www.sec.gov/Archives/edgar/data/1835714/0001085146-21-001095-index.html',
            'https://www.sec.gov/Archives/edgar/data/1446194/0001011712-21-000002-index.html']


class FlaskSqlAlchemyTestConfiguration(TestCase):
    """This class configures Flask SQL Alchemy"""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app = create_app(self)
        return app

    def setUp(self):
        db.create_all()
        self.company = Company(cik_no="509099898", company_name="Cool Industries", filing_count=0)
        self.edgar_filing = EdgarFiling(accession_no="0001420506-21-000830", cik_no="509099898",
                                     filing_date=datetime.fromisoformat("1999-09-01"))
        self.data_13f_table = [
            Data13f(equity_holdings_id = "67896567",
                    accession_no='0001420506-21-000830',
                    cik_no='0001171592',
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
        update_filing_count(self.company, self.edgar_filing)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskSQLAlchemyTest(FlaskSqlAlchemyTestConfiguration):
    """This class runs SQL ALchemy Tests"""
    def test_send_data_to_db_savesCompanyInDb(self):
        """This function tests if send_data_to_db saves the Company in the database"""
        send_data_to_db(self.company, self.edgar_filing, self.data_13f_table)

        assert self.company in db.session

    # def test_send_data_to_db_savesEdgarFilingInDb(self):
    #     send_data_to_db(self.company, self.edgar_filing, self.data_13f_table)
    #
    #     assert self.edgar_filing in db.session
    #
    # def test_send_data_to_db3(self):
    #     send_data_to_db(self.company, self.edgar_filing, self.data_13f_table)
    #
    #     assert self.data_13f_table in db.session
    #
    # def test_update_filing_count(self):
    #     company_1 = Company(cik_no="9099898", company_name="Backdoor Industries", filing_count=0)
    #     edgar_filing_1 = EdgarFiling(accession_no="7876789876", cik_no="9099898",
    #                                  filing_date=datetime.fromisoformat("1990-09-01"))
    #     company_2 = Company(cik_no="0984343", company_name="True Blue", filing_count=1)
    #     edgar_filing_2 = EdgarFiling(accession_no="87656789", cik_no="0984343",
    #                                  filing_date=datetime.fromisoformat("2002-04-10"))
    #     company_3 = Company(cik_no="8673434", company_name="Purple Company", filing_count=1)
    #     edgar_filing_3 = EdgarFiling(accession_no="3453456", cik_no="8673434",
    #                                  filing_date=datetime.fromisoformat("2000-06-11"))
    #     edgar_filing_4 = EdgarFiling(accession_no="3453456", cik_no="8673434",
    #                                  filing_date=datetime.fromisoformat("2000-06-11"))
    #     db.session.add(edgar_filing_1, company_1)
    #     db.session.commit()
    #
    #     # this works
    #     assert company_1 in db.session
    #
    #
