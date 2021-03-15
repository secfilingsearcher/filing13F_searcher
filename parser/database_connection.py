from sqlalchemy import create_engine
import os


def connect_to_database():
    db = create_engine(os.environ.get('DB_CONNECTION_STRING'))
    return db


def create_and_insert_to_database(db):
    # Create
    # db.execute("CREATE TABLE IF NOT EXISTS films1 (cik_id, nameOfIssuer, titleOfClass, cusip, value,"
    #            " sshPrnamt, sshPrnamtType, putCall, investmentDiscretion,"
    #            " otherManager, votingAuthority_Sole,"
    #            " votingAuthority_Shared, votingAuthority_None)")
    db.execute("CREATE TABLE IF NOT EXISTS infotable1 (name text, "
               "id_name int, "
               "id_name int, "               
               "13f_id int PRIMARY KEY)")

    db.execute("CREATE TABLE IF NOT EXISTS primary1 (name text, "
               "id_name int, "
               "id_name int, "               
               "13f_id int PRIMARY KEY)")

    db.execute("INSERT INTO infotable1 (id, name)"
               "VALUES (3, 'susan'), "
               "(5, 'delores')"
               "ON CONFLICT (id) DO NOTHING;"
               )

    db.execute("INSERT INTO primary1 (id, name)"
               "VALUES (3, 'susan'), "
               "(5, 'delores')"
               "ON CONFLICT (id) DO NOTHING;"
               )

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
