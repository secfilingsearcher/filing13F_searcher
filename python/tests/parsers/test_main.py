# pylint: disable=redefined-outer-name
from flask import Flask
from flask_testing import TestCase
import pytest
from parsers.main import create_url_list
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


class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        return create_app(self)

    def setUp(self):
        db.create_all()

    def insertInDB(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskSQLAlchemyTest(MyTest):

    def test_send_data_to_db(self):
        user = User()
        db.session.add(user)
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
