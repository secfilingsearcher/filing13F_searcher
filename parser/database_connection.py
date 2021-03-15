from sqlalchemy import create_engine
import os


def connect_to_database():
    db = create_engine(os.environ.get('DB_CONNECTION_STRING'))
    return db


def create_and_insert_to_database(db):
    # Create
    db.execute("CREATE TABLE IF NOT EXISTS infotable_test1 (accession_no int PRIMARY KEY, "
               "cik int, "
               "nameOfIssuer text, "
               "titleOfClass text, "
               "cusip text, "
               "value text, "
               "sshPrnamt text, "
               "sshPrnamtType text, "
               "putCall text, "
               "investmentDiscretion text, "
               "otherManager text, "
               "votingAuthority_Sole text, "
               "votingAuthority_Shared text, "
               "votingAuthority_None text) "
               )

    db.execute("CREATE TABLE IF NOT EXISTS primary_doc_test1 (cik int PRIMARY KEY, "
               "company_name int, "
               "filing_date date) "
               )

    # db.execute("INSERT INTO infotable_test1 (id, name)"
    #            "VALUES (3, 'susan'), "
    #            "(5, 'delores')"
    #            "ON CONFLICT (id) DO NOTHING;"
    #            )
    #
    # db.execute("INSERT INTO primary1 (id, name)"
    #            "VALUES (3, 'susan'), "
    #            "(5, 'delores')"
    #            "ON CONFLICT (id) DO NOTHING;"
    #            )


def update_database(db):
    # Update
    db.execute("UPDATE films SET title='Some2016Film' WHERE year='2016'")


def read_database(db):
    # Read
    result_set = db.execute("SELECT * FROM films")
    for r in result_set:
        print(r)


db1 = connect_to_database()
create_and_insert_to_database(db1)

# first grab data
# then format
# then use sql alchemy
# send to database
