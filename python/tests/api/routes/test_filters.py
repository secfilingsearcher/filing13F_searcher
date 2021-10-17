"""This file contains tests for routes' filters"""
import os
from datetime import datetime, date

from flask import Flask
from flask_testing import TestCase

from edgar_filing_searcher.api.routes.filters import filter_company_by_date, filter_edgar_filing_by_date
from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import EdgarFiling, Company, Data13f
from edgar_filing_searcher.parsers.main import send_data_to_db

COMPANY_CIK_1 = "0001171592"
ACCESSION_NO_TABLE1_ROW1 = '0001420506-21-000830'
ACCESSION_NO_TABLE1_ROW2 = '00016273506-21-000830'
COMPANY_CIK_2 = "0006734892"
ACCESSION_NO_2 = '000384934-14-0034330'
COMPANY_CIK_3 = "0008322302"
ACCESSION_NO_3 = '000238234-23-0238930'
FALSE_COMPANY_CIK = "1"


class FlaskSqlAlchemyTestConfiguration(TestCase):
    """This class configures Flask SQL Alchemy for Tests"""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        """Creates and pushes a context for a test"""
        configuration_file_obj = self
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 0
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        if configuration_file_obj:
            app.config.from_object(configuration_file_obj)
        db.init_app(app)
        return app

    def setUp(self):
        """Sets up a test database"""
        db.create_all()
        self.company1 = Company(cik_no=COMPANY_CIK_1, company_name="Cool Industries", filing_count=1)
        self.edgar_filing1_row1 = EdgarFiling(accession_no=ACCESSION_NO_TABLE1_ROW1, cik_no=COMPANY_CIK_1,
                                              filing_date=datetime.fromisoformat("1999-09-01"))
        self.data_13f_table1_row1 = [Data13f(equity_holdings_id="67896567",
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
                                             )]
        self.edgar_filing1_row2 = EdgarFiling(accession_no=ACCESSION_NO_TABLE1_ROW2, cik_no=COMPANY_CIK_1,
                                              filing_date=datetime.fromisoformat("1998-05-02"))
        self.data_13f_table1_row2 = [Data13f(equity_holdings_id="673326567",
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
                                             )]

        self.company2 = Company(cik_no=COMPANY_CIK_2, company_name="Nice Industries", filing_count=1)
        self.edgar_filing2 = EdgarFiling(accession_no=ACCESSION_NO_2, cik_no=COMPANY_CIK_2,
                                         filing_date=datetime.fromisoformat("2000-04-05"))
        self.data_13f_table2 = [Data13f(equity_holdings_id="4364347",
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
                                        )]

        self.company3 = Company(cik_no=COMPANY_CIK_3, company_name="Purple Industries", filing_count=1)
        self.edgar_filing3 = EdgarFiling(accession_no=ACCESSION_NO_3, cik_no=COMPANY_CIK_3,
                                         filing_date=datetime.fromisoformat("2001-07-05"))
        self.data_13f_table3 = [Data13f(equity_holdings_id="39023347",
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
                                        )]

        send_data_to_db(self.company1, self.edgar_filing1_row1, self.data_13f_table1_row1)
        send_data_to_db(self.company1, self.edgar_filing1_row2, self.data_13f_table1_row2)
        send_data_to_db(self.company2, self.edgar_filing2, self.data_13f_table2)
        send_data_to_db(self.company3, self.edgar_filing3, self.data_13f_table3)

    def tearDown(self):
        """Tears down test database"""
        db.session.remove()
        db.drop_all()


class FlaskSQLAlchemyTest(FlaskSqlAlchemyTestConfiguration):
    """This class runs SQLALchemy Tests"""

    def test_filter_company_by_date_startDateAndEndDate(self):
        """Test for filter_company_by_date with start date and end date argument"""
        query = Company.query
        start_date = '1999-01-01'
        end_date = "1999-12-31"

        actual = filter_company_by_date(query, start_date, end_date)

        assert actual.all() == [Company(cik_no='0001171592', company_name='Cool Industries', filing_count=1)]

    def test_filter_company_by_date_startDate(self):
        """Test for filter_company_by_date with start date argument"""
        query = Company.query
        start_date = '2000-01-01'

        actual = filter_company_by_date(query, start_date, None)

        assert actual.all() == [Company(cik_no='0006734892', company_name='Nice Industries', filing_count=1),
                                Company(cik_no='0008322302', company_name='Purple Industries', filing_count=1)]

    def test_filter_company_by_date_endDate(self):
        """Test for filter_company_by_date with end date argument"""
        query = Company.query
        end_date = "1999-12-31"

        actual = filter_company_by_date(query, None, end_date)

        assert actual.all() == [Company(cik_no='0001171592', company_name='Cool Industries', filing_count=1)]

    def test_filter_company_by_date_noArguments(self):
        """Test for filter_company_by_date with no argument"""
        query = Company.query

        actual = filter_company_by_date(query, None, None)

        assert actual.all() == [
            Company(cik_no='0001171592', company_name='Cool Industries', filing_count=1),
            Company(cik_no='0006734892', company_name='Nice Industries', filing_count=1),
            Company(cik_no='0008322302', company_name='Purple Industries', filing_count=1)]

    def test_filter_edgar_filing_by_date_startDateAndEndDate(self):
        """Test for filter_edgar_filing_by_date with start date and end date argument"""
        query = EdgarFiling.query
        start_date = '1999-01-01'
        end_date = "1999-12-31"

        actual = filter_edgar_filing_by_date(query, start_date, end_date)

        assert actual.all() == [EdgarFiling(accession_no='0001420506-21-000830', cik_no='0001171592', filing_type=None,
                                            filing_date=date(1999, 9, 1))]

    def test_filter_edgar_filing_by_date_startDate(self):
        """Test for filter_edgar_filing_by_date with start date argument"""
        query = EdgarFiling.query
        start_date = '2000-01-01'

        actual = filter_edgar_filing_by_date(query, start_date, None)

        assert actual.all() == [EdgarFiling(accession_no='000384934-14-0034330', cik_no='0006734892', filing_type=None,
                                            filing_date=date(2000, 4, 5)),
                                EdgarFiling(accession_no='000238234-23-0238930', cik_no='0008322302', filing_type=None,
                                            filing_date=date(2001, 7, 5))]

    def test_filter_edgar_filing_by_date_endDate(self):
        """Test for filter_edgar_filing_by_date with end date argument"""
        query = EdgarFiling.query
        end_date = "1999-12-31"

        actual = filter_edgar_filing_by_date(query, None, end_date)

        assert actual.all() == [EdgarFiling(accession_no='0001420506-21-000830', cik_no='0001171592', filing_type=None,
                                            filing_date=date(1999, 9, 1)),
                                EdgarFiling(accession_no='00016273506-21-000830', cik_no='0001171592', filing_type=None,
                                            filing_date=date(1998, 5, 2))]

    def test_filter_edgar_filing_by_date_noArguments(self):
        """Test for filter_edgar_filing_by_date with no arguments"""
        query = EdgarFiling.query

        actual = filter_edgar_filing_by_date(query, None, None)

        assert actual.all() == [EdgarFiling(accession_no='0001420506-21-000830', cik_no='0001171592', filing_type=None,
                                            filing_date=date(1999, 9, 1)),
                                EdgarFiling(accession_no='00016273506-21-000830', cik_no='0001171592', filing_type=None,
                                            filing_date=date(1998, 5, 2)),
                                EdgarFiling(accession_no='000384934-14-0034330', cik_no='0006734892', filing_type=None,
                                            filing_date=date(2000, 4, 5)),
                                EdgarFiling(accession_no='000238234-23-0238930', cik_no='0008322302', filing_type=None,
                                            filing_date=date(2001, 7, 5))]