import os

from models import Base
from orm import get_engine


def create_db():
    engine = get_engine(os.environ.get('DB_CONNECTION_STRING'), True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_db()