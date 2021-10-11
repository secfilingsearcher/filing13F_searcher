"""This file contains tests for routes"""

from datetime import datetime

import pytest

from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f


class FlaskSqlAlchemyTestConfiguration:
    """This class configures Flask SQL Alchemy for Tests"""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True


COMPANY_CIK_1 = "0001171592"
ACCESSION_NO_TABLE1_ROW1 = '0001420506-21-000830'
ACCESSION_NO_TABLE1_ROW2 = '00016273506-21-000830'
COMPANY_CIK_2 = "0006734892"
ACCESSION_NO_2 = '000384934-14-0034330'
COMPANY_CIK_3 = "0008322302"
ACCESSION_NO_3 = '000238234-23-0238930'
FALSE_COMPANY_CIK = "1"


@pytest.fixture
def client():
    app = create_app(FlaskSqlAlchemyTestConfiguration())
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            company1 = Company(cik_no=COMPANY_CIK_1, company_name="Cool Industries", filing_count=1)
            edgar_filing1_row1 = EdgarFiling(accession_no=ACCESSION_NO_TABLE1_ROW1, cik_no=COMPANY_CIK_1,
                                             filing_date=datetime.fromisoformat("1999-09-01"))
            data_13f_table1_row1 = Data13f(equity_holdings_id="67896567",
                                           accession_no=ACCESSION_NO_TABLE1_ROW1,
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
            edgar_filing1_row2 = EdgarFiling(accession_no=ACCESSION_NO_TABLE1_ROW2, cik_no=COMPANY_CIK_1,
                                             filing_date=datetime.fromisoformat("1998-05-02"))
            data_13f_table1_row2 = Data13f(equity_holdings_id="673326567",
                                           accession_no=ACCESSION_NO_TABLE1_ROW2,
                                           cik_no='3349665767',
                                           name_of_issuer='Flight Technologies',
                                           title_of_class='COM',
                                           cusip='0584GU101',
                                           value=34967078.5,
                                           ssh_prnamt=2670644,
                                           ssh_prnamt_type='None',
                                           put_call='None',
                                           investment_discretion='SOLE',
                                           other_manager='None',
                                           voting_authority_sole=4257078,
                                           voting_authority_shared=0,
                                           voting_authority_none=0
                                           )

            company2 = Company(cik_no=COMPANY_CIK_2, company_name="Nice Industries", filing_count=1)
            edgar_filing2 = EdgarFiling(accession_no=ACCESSION_NO_2, cik_no=COMPANY_CIK_2,
                                        filing_date=datetime.fromisoformat("2000-04-05"))
            data_13f_table2 = Data13f(equity_holdings_id="4364347",
                                      accession_no=ACCESSION_NO_2,
                                      cik_no='56443437',
                                      name_of_issuer='Moon Labs',
                                      title_of_class='COM',
                                      cusip='008346101',
                                      value=6599834078.5,
                                      ssh_prnamt=1804594,
                                      ssh_prnamt_type='None',
                                      put_call='None',
                                      investment_discretion='SOLE',
                                      other_manager='None',
                                      voting_authority_sole=54522278,
                                      voting_authority_shared=0,
                                      voting_authority_none=0
                                      )

            company3 = Company(cik_no=COMPANY_CIK_3, company_name="Purple Industries", filing_count=1)
            edgar_filing3 = EdgarFiling(accession_no=ACCESSION_NO_3, cik_no=COMPANY_CIK_3,
                                        filing_date=datetime.fromisoformat("2001-07-05"))
            data_13f_table3 = Data13f(equity_holdings_id="39023347",
                                      accession_no=ACCESSION_NO_3,
                                      cik_no='823902437',
                                      name_of_issuer='Star Companies',
                                      title_of_class='COM',
                                      cusip='00923801',
                                      value=9023734078.5,
                                      ssh_prnamt=389594,
                                      ssh_prnamt_type='None',
                                      put_call='None',
                                      investment_discretion='SOLE',
                                      other_manager='None',
                                      voting_authority_sole=9823278,
                                      voting_authority_shared=0,
                                      voting_authority_none=0
                                      )

            db.session.add(company1)
            db.session.add(company2)
            db.session.add(company3)
            db.session.add(edgar_filing1_row1)
            db.session.add(edgar_filing1_row2)
            db.session.add(edgar_filing2)
            db.session.add(edgar_filing3)
            db.session.add(data_13f_table1_row1)
            db.session.add(data_13f_table1_row2)
            db.session.add(data_13f_table2)
            db.session.add(data_13f_table3)
            db.session.commit()
        yield client


def test_search_company_qArgument_responseCode(client):
    """Test for the response code for search_company function for the q argument"""
    response = client.get('/company/search?q=Cool')
    assert response.status_code == 200


def test_search_company_qArgument_json(client):
    """Test for the json for search_company function for the q argument"""
    response = client.get('/company/search?q=Cool')
    assert response.get_json() == [{'cik_no': '0001171592', 'company_name': 'Cool Industries', 'filing_count': 1}]


def test_search_company_qArgument_startDateAndEndDate_responseCode(client):
    """Test for the response code for search_company function for the q, start date, and end date argument"""
    response = client.get('/company/search?q=&start_date=2000-04-05&end_date=2000-04-05')
    assert response.status_code == 200


def test_search_company_qArgument_startDateAndEndDate_json(client):
    """Test for the json for search_company function for the q, start date, and end date argument"""
    response = client.get('/company/search?q=&start_date=2000-04-05&end_date=2000-04-05')
    assert response.get_json() == [{'cik_no': '0006734892', 'company_name': 'Nice Industries', 'filing_count': 1}]


def test_search_company_qArgument_startDate_responseCode(client):
    """Test for the response code for search_company function for the q and start date argument"""
    response = client.get('/company/search?q=&start_date=2001-01-01')
    assert response.status_code == 200


def test_search_company_qArgument_startDate_json(client):
    """Test for the json for search_company function for the q and start date argument"""
    response = client.get('/company/search?q=&start_date=2001-01-01')
    assert response.get_json() == [{'cik_no': '0008322302', 'company_name': 'Purple Industries', 'filing_count': 1}]


def test_search_company_qArgument_endDate_responseCode(client):
    """Test for the response code for search_company function for the q and end date argument"""
    response = client.get('/company/search?q=&end_date=1999-12-31')
    assert response.status_code == 200


def test_search_company_qArgument_endDate_json(client):
    """Test for the json  for search_company function for the q and end date argument"""
    response = client.get('/company/search?q=&end_date=1999-12-31')
    assert response.get_json() == [{'cik_no': '0001171592', 'company_name': 'Cool Industries', 'filing_count': 1}]


def test_search_company_companyNameArgument_responseCode(client):
    """Test for the response code for search_company function for the company name argument"""
    response = client.get('/company/search?company_name=Cool')
    assert response.status_code == 200


def test_search_company_companyNameArgument_json(client):
    """Test for the json for the json for search_company function for the company name argument"""
    response = client.get('/company/search?company_name=Cool')
    assert response.get_json() == [{'cik_no': '0001171592', 'company_name': 'Cool Industries', 'filing_count': 1}]


def test_search_company_companyNameArgument_startDateAndEndDate_responseCode(client):
    """Test for the response code for search_company function for the company name, start date, and end date argument"""
    response = client.get('/company/search?company_name=&start_date=2000-04-05&end_date=2000-04-05')
    assert response.status_code == 200


def test_search_company_companyNameArgument_startDateAndEndDate_json(client):
    """Test for the json for search_company function for the company name, start date, and end date argument"""
    response = client.get('/company/search?company_name=&start_date=2000-04-05&end_date=2000-04-05')
    assert response.get_json() == [{'cik_no': '0006734892', 'company_name': 'Nice Industries', 'filing_count': 1}]


def test_search_company_companyNameArgument_startDate_responseCode(client):
    """Test for the response code for search_company function for the company name and start date argument"""
    response = client.get('/company/search?company_name=&start_date=2001-01-01')
    assert response.status_code == 200


def test_search_company_companyNameArgument_startDate_json(client):
    """Test for the json for the start date for search_company function for the company name and start date argument"""
    response = client.get('/company/search?company_name=&start_date=2001-01-01')
    assert response.get_json() == [{'cik_no': '0008322302', 'company_name': 'Purple Industries', 'filing_count': 1}]


def test_search_company_companyNameArgument_endDate_responseCode(client):
    """Test for the response code for search_company function for the company name and end date argument"""
    response = client.get('/company/search?company_name=&end_date=1999-12-31')
    assert response.status_code == 200


def test_search_company_companyNameArgument_endDate_json(client):
    """Test for the json for search_company function for the company name and end date argument"""
    response = client.get('/company/search?company_name=&end_date=1999-12-31')
    assert response.get_json() == [{'cik_no': '0001171592', 'company_name': 'Cool Industries', 'filing_count': 1}]


def test_search_company_nameOfIssuerArgument_responseCode(client):
    """Test for the response code for search_company function for the name of issuer argument"""
    response = client.get('/company/search?name_of_issuer=Agilent')
    assert response.status_code == 200


def test_search_company_nameOfIssuerArgument_json(client):
    """Test for the json for the json for search_company function for the name of issuer argument"""
    response = client.get('/company/search?name_of_issuer=Agilent')
    assert response.get_json() == [{'cik_no': '0001171592', 'company_name': 'Cool Industries', 'filing_count': 1}]


def test_search_company_nameOfIssuerArgument_startDateAndEndDate_responseCode(client):
    """Test for the response code for search_company function
    for the name of issuer, start date, and end date argument"""
    response = client.get('/company/search?name_of_issuer=Agilent&start_date=1999-01-01&end_date=1999-12-31')
    assert response.status_code == 200


def test_search_company_nameOfIssuerArgument_startDateAndEndDate_json(client):
    """Test for the json for search_company function
    for the name of issuer, start date, and end date argument"""
    response = client.get('/company/search?name_of_issuer=Agilent&start_date=1999-01-01&end_date=1999-12-31')
    assert response.get_json() == [{'cik_no': '0001171592', 'company_name': 'Cool Industries', 'filing_count': 1}]


def test_search_company_nameOfIssuerArgument_startDate_responseCode(client):
    """Test for the response code for search_company function for the name of issuer and start date argument"""
    response = client.get('/company/search?name_of_issuer=Agilent&start_date=1999-01-01&end_date=1999-12-31')
    assert response.status_code == 200


def test_search_company_nameOfIssuerArgument_startDate_json(client):
    """Test for the json for search_company function for the name of issuer and start date argument"""
    response = client.get('/company/search?name_of_issuer=Moon&start_date=1999-01-01')
    assert response.get_json() == [{'cik_no': '0006734892', 'company_name': 'Nice Industries', 'filing_count': 1}]


def test_search_company_nameOfIssuerArgument_endDate_responseCode(client):
    """Test for the response code for search_company function for the name of issuer and end date argument"""
    response = client.get('/company/search?name_of_issuer=Star&end_date=2001-12-31')
    assert response.status_code == 200


def test_search_company_nameOfIssuerArgument_endDate_json(client):
    """Test for the json for search_company function for the name of issuer and end date argument"""
    response = client.get('/company/search?name_of_issuer=Star&end_date=2001-12-31')
    assert response.get_json() == [{'cik_no': '0008322302', 'company_name': 'Purple Industries', 'filing_count': 1}]


def test_search_company_noArguments_responseCode(client):
    """Test for the response code for search_company function with no argument"""
    response = client.get('/company/search')
    assert response.status_code == 400


def test_search_company_noArguments_json(client):
    """Test for the json for json for search_company function with no argument"""
    response = client.get('/company/search')
    assert response.get_json() is None


def test_get_edgarfilings_with_date_responseCode(client):
    """Test for the response code for get_edgarfilings_with_date function"""
    response = client.get(f'/company/{COMPANY_CIK_1}/edgar-filing/')
    assert response.status_code == 200


def test_get_edgarfilings_with_date_json(client):
    """Test for the json for get_edgarfilings_with_date function"""
    response = client.get(f'/company/{COMPANY_CIK_1}/edgar-filing/')
    assert response.get_json() == [{'accession_no': '0001420506-21-000830',
                                    'cik_no': '0001171592',
                                    'filing_date': 'Wed, 01 Sep 1999 00:00:00 GMT',
                                    'filing_type': None},
                                   {'accession_no': '00016273506-21-000830',
                                    'cik_no': '0001171592',
                                    'filing_date': 'Sat, 02 May 1998 00:00:00 GMT',
                                    'filing_type': None}]


def test_get_edgarfilings_with_date_startDateAndEndDate_responseCode(client):
    """Test for the response code for get_edgarfilings_with_date function with start date and end date argument"""
    response = client.get(f'/company/{COMPANY_CIK_1}/edgar-filing/'
                          f'?start_date=1999-01-01&end_date=1999-12-31')
    assert response.status_code == 200


def test_get_edgarfilings_with_date_startDateAndEndDate_json(client):
    """Test for the json for get_edgarfilings_with_date function with start date and end date argument"""
    response = client.get(f'/company/{COMPANY_CIK_1}/edgar-filing/'
                          f'?start_date=1999-01-01&end_date=1999-12-31')
    assert response.get_json() == [{'accession_no': '0001420506-21-000830',
                                    'cik_no': '0001171592',
                                    'filing_date': 'Wed, 01 Sep 1999 00:00:00 GMT',
                                    'filing_type': None}]


def test_get_edgarfilings_with_date_startDate_responseCode(client):
    """Test for the response code for get_edgarfilings_with_date function with start date argument"""
    response = client.get(f'/company/{COMPANY_CIK_1}/edgar-filing/?start_date=1999-01-01')
    assert response.status_code == 200


def test_get_edgarfilings_with_date_startDate_json(client):
    """Test for the json for the start date for get_edgarfilings_with_date function with start date argument"""
    response = client.get(f'/company/{COMPANY_CIK_1}/edgar-filing/?start_date=1999-01-01')
    assert response.get_json() == [{'accession_no': '0001420506-21-000830',
                                    'cik_no': '0001171592',
                                    'filing_date': 'Wed, 01 Sep 1999 00:00:00 GMT',
                                    'filing_type': None}]


def test_get_edgarfilings_with_date_endDate_responseCode(client):
    """Test for the response code for get_edgarfilings_with_date function with end date argument"""
    response = client.get(f'/company/{COMPANY_CIK_1}/edgar-filing/?end_date=1998-12-31')
    assert response.status_code == 200


def test_get_edgarfilings_with_date_endDate_json(client):
    """Test for the json for get_edgarfilings_with_date function with end date argument"""
    response = client.get(f'/company/{COMPANY_CIK_1}/edgar-filing/?end_date=1998-12-31')
    assert response.get_json() == [{'accession_no': '00016273506-21-000830',
                                    'cik_no': '0001171592',
                                    'filing_date': 'Sat, 02 May 1998 00:00:00 GMT',
                                    'filing_type': None}]


def test_get_edgarfilings_by_filing_id_responseCode(client):
    """Test for the response code for get_edgarfilings_with_date function"""
    response = client.get(f'/edgar-filing/{ACCESSION_NO_TABLE1_ROW1}/data/')
    assert response.status_code == 200


def test_get_edgarfilings_by_filing_id_json(client):
    """Test for the json for get_edgarfilings_with_date function"""
    response = client.get(f'/edgar-filing/{ACCESSION_NO_TABLE1_ROW1}/data/')
    assert response.get_json() == [{'equity_holdings_id': '67896567',
                                    'accession_no': '0001420506-21-000830',
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


def test_get_company_by_company_id_responseCode(client):
    """Test for the response code for get_company_by_company_id function"""
    response = client.get(f'/company/{COMPANY_CIK_1}')
    assert response.status_code == 200


def test_get_company_by_company_id_json(client):
    """Test for the json for get_company_by_company_id function"""
    response = client.get(f'/company/{COMPANY_CIK_1}')
    assert response.get_json() == {'cik_no': '0001171592', 'company_name': 'Cool Industries', 'filing_count': 1}


def test_get_company_by_company_id_false_company_id(client):
    """Test for the json for get_company_by_company_id function with false company_id"""
    response = client.get(f'/company/{FALSE_COMPANY_CIK}')
    assert response.status_code == 404
