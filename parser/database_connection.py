"""Create database connection"""
import os
from typing import List
from sqlalchemy.orm import sessionmaker
from orm import get_engine

engine = get_engine(os.environ.get('DB_CONNECTION_STRING'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def add_to_session_primary_table(row):
    """Add primary_doc rows to session"""
    session.add(row)


def add_to_session_infotable_table(infotable_table: List):
    """Add infotable rows to session"""
    session.add_all(infotable_table)


def commit_to_database():
    """Commit rows to database"""
    session.commit()
