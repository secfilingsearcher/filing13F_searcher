"""WSGI entry point"""
from edgar_filing_searcher.api import create_app

app = create_app()
