"""Delete EdgarFilings data with missing Data13f data"""
from models import EdgarFiling, Data13f
from parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.database import db

setup_db_connection()

all_edgar_filing_accession_no = EdgarFiling.query.with_entities(EdgarFiling.accession_no).group_by(
    EdgarFiling.accession_no).all()
all_data13f_accession_no = Data13f.query.with_entities(Data13f.accession_no).group_by(
    Data13f.accession_no).all()

set_of_data13f_accession_no = set()
for row in all_data13f_accession_no:
    for data13f_accession_no in row:
        set_of_data13f_accession_no.add(data13f_accession_no)
set_of_edgar_filing_accession_no = set()
for row in all_edgar_filing_accession_no:
    for edgar_filing_accession_no in row:
        set_of_edgar_filing_accession_no.add(edgar_filing_accession_no)

difference = set_of_edgar_filing_accession_no.difference(set_of_data13f_accession_no)
print("Number of filings with missing data: ", len(difference))

for accession_no in difference:
    dates_with_missing_data = EdgarFiling.query \
        .filter(EdgarFiling.accession_no == accession_no).delete()
    db.session.commit()
    print(f"Accession number {accession_no} deleted from EdgarFiling.")
