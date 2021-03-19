"""docstring"""
import os
from sqlalchemy.orm import sessionmaker
import pandas as pd
from models import PrimaryDoc
from orm import get_engine

engine = get_engine(os.environ.get('DB_CONNECTION_STRING'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def insert_in_primary_table(id, cik, company_name, filing_date):
    """docstring"""
    session.add(PrimaryDoc(id=id, cik=cik, company_name=company_name, filing_date=filing_date))
    session.commit()


def insert_in_infotable_table(engine, df: pd.DataFrame):
    """docstring"""
    df.to_sql(name='infotable', con=engine, if_exists="fail")
