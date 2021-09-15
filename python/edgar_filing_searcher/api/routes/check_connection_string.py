""""""
import logging
import os
import psycopg2

from edgar_filing_searcher.parsers.errors import InvalidConnectionStringException


def postgres_test():
    """"""
    try:
        conn = psycopg2.connect(os.environ.get('DB_CONNECTION_STRING'))
        conn.close()
        logging.info('%s Connection Successful', conn)
    except:
        logging.critical("Invalid Url")
        raise InvalidConnectionStringException("Invalid Database Connection String Url")