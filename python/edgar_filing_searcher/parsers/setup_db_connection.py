"""This file sets up the database connection"""
from edgar_filing_searcher.parsers.parser_context import create_app

def setup_db_connection():
    """This function creates and pushes a context"""
    app = create_app()
    app.app_context().push()
