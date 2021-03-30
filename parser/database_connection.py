"""Create database connection"""
import os
from typing import List

from sqlalchemy.orm import sessionmaker
from models import PrimaryDoc
from orm import get_engine

engine = get_engine(os.environ.get('DB_CONNECTION_STRING'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def insert_in_database_primary_table(primary_key_id, cik, company_name, filing_date):
    """Insert list in primary_doc table"""
    session.add(PrimaryDoc(id=primary_key_id, cik=cik,
                           company_name=company_name, filing_date=filing_date))
    session.commit()


def insert_in_database_infotable_table(infotable_table: List):
    """Insert dataframe in infotable table"""
    session.add_all(infotable_table)
    session.commit()
