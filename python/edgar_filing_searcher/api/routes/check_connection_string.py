"""This file checks the connection string"""
import logging
import psycopg2

from edgar_filing_searcher.parsers.errors import InvalidConnectionStringException


def check_postgres_connection_string(db_connection_string: str):
    """This function checks the connection string"""
    try:
        conn = psycopg2.connect(db_connection_string)
        conn.close()
        logging.info('%s Connection Successful', conn)
    except Exception as error:
        logging.critical("Invalid Url")
        raise InvalidConnectionStringException("Invalid Database Connection String Url") from error
