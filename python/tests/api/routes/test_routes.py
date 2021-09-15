"""This file contains tests for main"""

from datetime import datetime

import pytest

from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f


class FlaskSqlAlchemyTestConfiguration:
    """This class configures Flask SQL Alchemy for Tests"""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True


COMPANY_CIK = "0001171592"
ACCESSION_NO = '0001420506-21-000830'


@pytest.fixture
def client():
    app = create_app(FlaskSqlAlchemyTestConfiguration())
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            company = Company(cik_no=COMPANY_CIK, company_name="Cool Industries", filing_count=1)
            edgar_filing = EdgarFiling(accession_no="0001420506-21-000830", cik_no=COMPANY_CIK,
                                       filing_date=datetime.fromisoformat("1999-09-01"))
            data_13f_table = Data13f(equity_holdings_id="67896567",
                                     accession_no=ACCESSION_NO,
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
                                     )

            db.session.add(company)
            db.session.add(edgar_filing)
            db.session.add(data_13f_table)
            db.session.commit()
        yield client


def test_search_company_has_arguments_responseCode(client):
    response = client.get('/company/search?q=c')
    assert response.status_code == 200


def test_search_company_has_arguments_json(client):
    response = client.get('/company/search?q=c')
    assert response.get_json() == [{'cik_no': '0001171592', 'company_name': 'Cool Industries', 'filing_count': 1}]


def test_search_company_has_no_arguments_responseCode(client):
    response = client.get('/company/search')
    assert response.status_code == 400


def test_search_company_has_no_arguments_json(client):
    response = client.get('/company/search')
    assert response.get_json() is None


def test_get_edgarfilings_with_date_responseCode(client):
    response = client.get(f'/company/{COMPANY_CIK}/edgarfiling/')
    assert response.status_code == 200


def test_get_edgarfilings_with_date_json(client): 
    response = client.get(f'/company/{COMPANY_CIK}/edgarfiling/')
    assert response.get_json() == [{'accession_no': '0001420506-21-000830',
                                    'cik_no': '0001171592',
                                    'filing_date': 'Wed, 01 Sep 1999 00:00:00 GMT'}]


def test_get_edgarfilings_with_date_DateBehavior(client): 
    response = client.get(f'/company/{COMPANY_CIK}/edgarfiling/')
    assert response.get_json() == [{'accession_no': '0001420506-21-000830',
                                    'cik_no': '0001171592',
                                    'filing_date': 'Wed, 01 Sep 1999 00:00:00 GMT'}]


def test_get_edgarfilings_by_accession_no_responseCode(client):
    response = client.get(f'/edgarfiling/{ACCESSION_NO}/data/')
    assert response.status_code == 200


def test_get_edgarfilings_by_accession_no_json(client):
    response = client.get(f'/edgarfiling/{ACCESSION_NO}/data/')
    assert response.get_json() == [{'accession_no': '0001420506-21-000830',
                                    'cik_no': '56464565767',
                                    'cusip': '00846U101',
                                    'investment_discretion': 'SOLE',
                                    'name_of_issuer': 'Agilent Technologies',
                                    'other_manager': 'None',
                                    'put_call': 'None',
                                    'ssh_prnamt': 180644,
                                    'ssh_prnamt_type': 'None',
                                    'title_of_class': 'COM',
                                    'value': 22967078.5,
                                    'voting_authority_none': 0,
                                    'voting_authority_shared': 0,
                                    'voting_authority_sole': 22967078}]
