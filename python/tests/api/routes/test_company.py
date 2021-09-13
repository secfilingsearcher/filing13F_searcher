"""This file contains tests for main"""

import pytest
from datetime import datetime
from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f


class FlaskSqlAlchemyTestConfiguration:
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


@pytest.fixture
def client():
    app = create_app(FlaskSqlAlchemyTestConfiguration())
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_search_company_HasArguments(client):
    response = client.get('/company/search?q=c')
    assert response.status_code == 200
    assert response.get_json() == []


def test_search_company_HasNoArguments(client):
    response = client.get('/company/search')
    assert response.status_code == 400
    assert response.get_json() is None


def test_search_filings_with_date(client):
    response = client.get('/company/0001171592/edgarfiling/')
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_filings_from_company_id(client):
    response = client.get('/company/0001171592/')
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_filings_from_company_id_and_filing_id(client):
    response = client.get('/company/0001171592/filing/0001420506-21-000830')
    assert response.status_code == 200
    assert response.get_json() == []
