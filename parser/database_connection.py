from sqlalchemy import create_engine
import os


def connect_to_database():
    db = create_engine(os.environ.get('DB_CONNECTION_STRING'))
    return db


def create_database(db):
    # Create
    db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")
    db.execute("INSERT INTO films (title, director, year) "
               "VALUES ('Doctor Strange', 'Scott Derrickson', '2016')")


def update_database(db):
    # Update
    db.execute("UPDATE films SET title='Some2016Film' WHERE year='2016'")


def read_database(db):
    # Read
    result_set = db.execute("SELECT * FROM films")
    for r in result_set:
        print(r)


# first grab data
# then format
# then use sql alchemy
# send to database
