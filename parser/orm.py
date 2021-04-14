"""Launch Object Relational Mapper"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(db_uri, echo=False):
    """Creating an sqlalchemy engine"""
    engine = create_engine(db_uri, echo=echo)
    return engine


def get_session(db_uri):
    """Create a top level Session configuration which can then be used throughout"""
    return sessionmaker(bind=get_engine(db_uri))()
