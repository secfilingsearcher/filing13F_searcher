"""docstring"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(db_uri, echo=False):
    """docstring"""
    engine = create_engine(db_uri, echo=echo)
    return engine


def get_session(db_uri):
    """docstring"""
    return sessionmaker(bind=get_engine(db_uri))()
