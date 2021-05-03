"""Create database connection"""
import os
from sqlalchemy.orm import sessionmaker
from edgar_filing_searcher.parsers.orm import get_engine

engine = get_engine(os.environ.get('DB_CONNECTION_STRING'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
