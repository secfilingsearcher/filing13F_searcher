"""Initialize Database"""
from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db

if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    db.create_all()
