from sqlalchemy import create_engine
import os
import pandas as pd


def connect_to_database():
    engine = create_engine(os.environ.get('DB_CONNECTION_STRING'))
    return engine


def create_table(engine):
    # Create
    engine.execute("CREATE TABLE IF NOT EXISTS infotable_test3 (accession_no int PRIMARY KEY, "
                   "cik int, "
                   "nameOfIssuer text, "
                   "titleOfClass text, "
                   "cusip text, "
                   "value money, "
                   "sshPrnamt int, "
                   "sshPrnamtType text, "
                   "putCall text, "
                   "investmentDiscretion text, "
                   "otherManager text, "
                   "votingAuthority_Sole int, "
                   "votingAuthority_Shared int, "
                   "votingAuthority_None int) "
                   )

    engine.execute("CREATE TABLE IF NOT EXISTS primary_doc_test1 (cik int PRIMARY KEY, "
                   "company_name int, "
                   "filing_date date) "
                   )


def insert_in_table(engine, df):
    df.to_sql('infotable_test3', engine)

    engine.execute("INSERT INTO primary_doc_test1 (cik, company_name)"
                   "VALUES (3, 'susan'), "
                   "(5, 'delores')"
                   "ON CONFLICT (cik) DO NOTHING;"
                   )


def update_database(engine):
    # Update
    engine.execute("UPDATE films SET title='Some2016Film' WHERE year='2016'")


def read_database(engine):
    # Read
    result_set = engine.execute("SELECT * FROM films")
    for r in result_set:
        print(r)


engine1 = connect_to_database()
create_table(engine1)

# first grab data
# then format
# then use sql alchemy
# send to database
