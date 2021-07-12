"""This file sets up the database connection"""
import logging
from edgar_filing_searcher.parsers.parser_context import create_app


def setup_db_connection():
    """This function creates and pushes a context"""
    logging.debug('Start database connection')
    app = create_app()
    app.app_context().push()
    logging.debug('Database connection set up')

