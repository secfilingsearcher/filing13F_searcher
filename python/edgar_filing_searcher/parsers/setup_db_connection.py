from edgar_filing_searcher.parsers.parser_context import create_app

def setup_db_connection():
    app = create_app()
    app.app_context().push()