"""Initialize Database"""
from edgar_filing_searcher.api.database import db
from edgar_filing_searcher.api import create_app


if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    db.create_all()
