# pylint: disable=redefined-outer-name
from datetime import datetime
from flask import Flask
from flask_testing import TestCase
import pytest
from models import EdgarFiling, Company, Data13f
from parsers.main import create_url_list, send_data_to_db
from edgar_filing_searcher.database import db
from edgar_filing_searcher.api import create_app
from unittest.mock import patch, MagicMock

"""This file contains tests for main"""


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
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskSQLAlchemyTest(FlaskSqlAlchemyTestConfiguration):
    def test_send_data_to_db(self):
        company_row = Company(cik_no="509099898", company_name="Cool Industries", filing_count=0)
        edgar_filing_row = EdgarFiling(accession_no="4576789876", cik_no="509099898",
                                       filing_date=datetime.fromisoformat("1999-09-01"))
        values = [Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Agilent Technologies', title_of_class='COM', cusip='00846U101', value='22967078', ssh_prnamt='180644', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='22967078', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Air Lease Corp.', title_of_class='COM', cusip='00912X302', value='17782198', ssh_prnamt='362902', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='17782198', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Albemarle', title_of_class='COM', cusip='012653101', value='9503725', ssh_prnamt='65045', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='9503725', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Alexandria Real Estate Equities', title_of_class='COM', cusip='015271109', value='13324073', ssh_prnamt='81096', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='13324073', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Bank of N.T. Butterfield & Sons', title_of_class='COM', cusip='G0772R208', value='9475197', ssh_prnamt='247912', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='9475197', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Becton Dickinson', title_of_class='COM', cusip='075887109', value='15954774', ssh_prnamt='65617', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='15954774', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Black Knight, Inc.', title_of_class='COM', cusip='09215C105', value='4183321', ssh_prnamt='56539', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='4183321', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='CBRE Group', title_of_class='COM', cusip='12504L109', value='24385974', ssh_prnamt='308254', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='24385974', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='CIT Group', title_of_class='COM', cusip='125581801', value='6266604', ssh_prnamt='121658', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='6266604', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Carter's', title_of_class='COM', cusip='146229109', value='10019743', ssh_prnamt='112670', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='10019743', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='East West Bancorp', title_of_class='COM', cusip='27579R104', value='18948150', ssh_prnamt='256750', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='18948150', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Emcor Group', title_of_class='COM', cusip='29084Q100', value='14226599', ssh_prnamt='126842', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='14226599', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Equinix Inc.', title_of_class='COM', cusip='29444U700', value='16248317', ssh_prnamt='23909', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='16248317', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Euronet Worldwide', title_of_class='COM', cusip='298736109', value='22473750', ssh_prnamt='162500', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='22473750', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Fidelity National Financial', title_of_class='COM', cusip='31620R303', value='7397680', ssh_prnamt='181940', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='7397680', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='First Republic Bank', title_of_class='COM', cusip='33616C100', value='14565779', ssh_prnamt='87351', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='14565779', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Genpact Ltd.', title_of_class='COM', cusip='G3922B107', value='17075760', ssh_prnamt='398780', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='17075760', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Hexcel', title_of_class='COM', cusip='428291108', value='11914392', ssh_prnamt='212757', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='11914392', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='IDEX Corporation', title_of_class='COM', cusip='45167R104', value='2482745', ssh_prnamt='11861', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='2482745', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Jacobs Engineering', title_of_class='COM', cusip='469814107', value='21490879', ssh_prnamt='166248', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='21490879', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Keysight Technologies, Inc.', title_of_class='COM', cusip='49338L103', value='19378933', ssh_prnamt='135139', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='19378933', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Laboratory Corp. of America Holdings', title_of_class='COM', cusip='50540R409', value='20917816', ssh_prnamt='82021', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='20917816', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Liberty Media Corp - Formula One', title_of_class='COM', cusip='531229854', value='6247396', ssh_prnamt='144315', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='6247396', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Mid-America Apartment Communities', title_of_class='COM', cusip='59522J103', value='18757272', ssh_prnamt='129934', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='18757272', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Mohawk Industries', title_of_class='COM', cusip='608190104', value='9757040', ssh_prnamt='50736', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='9757040', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='PVH Corp', title_of_class='COM', cusip='693656100', value='11418560', ssh_prnamt='108028', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='11418560', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Roper Industries', title_of_class='COM', cusip='776696106', value='9963305', ssh_prnamt='24702', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='9963305', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Ross Stores', title_of_class='COM', cusip='778296103', value='19896187', ssh_prnamt='165926', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='19896187', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='SBA Communications Corp', title_of_class='COM', cusip='78410G104', value='9549108', ssh_prnamt='34405', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='9549108', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='SEI Investments', title_of_class='COM', cusip='784117103', value='11297397', ssh_prnamt='185416', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='11297397', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='SLM Corp', title_of_class='COM', cusip='78442P106', value='19005701', ssh_prnamt='1057635', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='19005701', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Virtu Financial', title_of_class='COM', cusip='928254101', value='10334868', ssh_prnamt='332846', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='10334868', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Wabtec', title_of_class='COM', cusip='929740108', value='4337572', ssh_prnamt='54795', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='4337572', voting_authority_shared='0', voting_authority_none='0'), Data13f(accession_no='0001420506-21-000830', cik_no='0001171592', name_of_issuer='Xilinx Inc', title_of_class='COM', cusip='983919101', value='8172816', ssh_prnamt='65963', ssh_prnamt_type='None', putCall='None', investment_discretion='SOLE', other_manager='None', voting_authority_sole='8172816', voting_authority_shared='0', voting_authority_none='0')]
        data_13f_row = Data13f()
        (equity_holdings_id="kk"), accession_no=, cik_no=, name_of_issuer=, title_of_class, cusip=,
                                 value=, ssh_prnamt=, ssh_prnamt_type=, put_call=, investment_discretion=,
                                 other_manager=, voting_authority_sole=, voting_authority_shared=,
                                 voting_authority_none=)

        send_data_to_db(company_row, edgar_filing_row, data_13f_table)
        # this works
        assert company_row, edgar_filing_row, data_13f_table in db.session
        response = self.client.get("/")

    def test_update_filing_count(self):
        company_1 = Company(cik_no="9099898", company_name="Backdoor Industries", filing_count=0)
        edgar_filing_1 = EdgarFiling(accession_no="7876789876", cik_no="9099898",
                                     filing_date=datetime.fromisoformat("1990-09-01"))
        company_2 = Company(cik_no="0984343", company_name="True Blue", filing_count=1)
        edgar_filing_2 = EdgarFiling(accession_no="87656789", cik_no="0984343",
                                     filing_date=datetime.fromisoformat("2002-04-10"))
        company_3 = Company(cik_no="8673434", company_name="Purple Company", filing_count=1)
        edgar_filing_3 = EdgarFiling(accession_no="3453456", cik_no="8673434",
                                     filing_date=datetime.fromisoformat("2000-06-11"))
        edgar_filing_4 = EdgarFiling(accession_no="3453456", cik_no="8673434",
                                     filing_date=datetime.fromisoformat("2000-06-11"))
        db.session.add(edgar_filing_1, company_1)
        db.session.commit()

        # this works
        assert user in db.session

        response = self.client.get("/")

        # this raises an AssertionError
        assert user in db.session


#
# def test_send_data_to_db():
#     """This function tests send_data_to_db"""
#     assert False


class MyTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
