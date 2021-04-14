import os
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(connection_string, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, ))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import PrimaryDoc, Infotable
    Base.metadata.create_all(bind=engine)