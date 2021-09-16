"""This file checks the connection string"""
from sqlalchemy import create_engine

from edgar_filing_searcher.errors import InvalidConnectionStringException


def check_connection_string(db_connection_string: str):
    """This function checks the connection string"""
    try:
        some_engine = create_engine(db_connection_string)
        conn = some_engine.connect()
        conn.close()
    except Exception as error:
        raise InvalidConnectionStringException(error, "Invalid Database Connection String Url")
