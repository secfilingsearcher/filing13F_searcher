# pylint: disable=redefined-outer-name
"""This file contains tests for crawler_current_events"""
import os
import pytest
from edgar_filing_searcher.api.routes.check_connection_string import postgres_test
from edgar_filing_searcher.parsers.errors import InvalidConnectionStringException

from datetime import datetime
from flask_testing import TestCase
from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f


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
                                      voting_authority_none='0'
                                      )
        db.session.merge(self.company)
        db.session.merge(self.edgar_filing)
        db.session.merge(self.data_13f_table)
        db.session.commit()

    def tearDown(self):
        """Tears down test database"""
        db.session.remove()
        db.drop_all()


class FlaskSQLAlchemyTest(FlaskSqlAlchemyTestConfiguration):
    """This class runs SQLALchemy Tests"""

    def test_postgres_test(self):
        """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
        os.environ["DB_CONNECTION_STRING"] = "sqlite://"
        actual = postgres_test()
        assert actual == \
               ['https://www.sec.gov/Archives/edgar/data/1850858/0001850858-21-000001-index.html']

    def test_check_connection_string_invalidConnectionString_raiseException(self):
        """Tests if parse_13f_filing_detail_urls raises the NoUrlException exception"""
        os.environ["DB_CONNECTION_STRING"] = ""
        with pytest.raises(InvalidConnectionStringException):
            postgres_test()
