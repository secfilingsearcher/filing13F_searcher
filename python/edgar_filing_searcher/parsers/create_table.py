"""Create table in database"""
import os
from edgar_filing_searcher.parsers.models import Base
from edgar_filing_searcher.parsers.orm import get_engine


def create_db():
    """Create connection to database to create a table using classes on model.py"""
    engine = get_engine(os.environ.get('DB_CONNECTION_STRING'), True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_db()
