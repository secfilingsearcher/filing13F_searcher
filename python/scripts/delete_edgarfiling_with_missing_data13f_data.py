"""Delete edgarfiling with missing data13f data"""
from models import EdgarFiling, Data13f
from parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.database import db

setup_db_connection()

edgar_filing_accession_no_results = EdgarFiling.query.with_entities(EdgarFiling.accession_no).group_by(
    EdgarFiling.accession_no).all()
data13f_accession_no_results = Data13f.query.with_entities(Data13f.accession_no).group_by(
    Data13f.accession_no).all()

set_of_data13f_accession_no = set()
for row in data13f_accession_no_results:
    for data13f_accession_no in row:
        set_of_data13f_accession_no.add(data13f_accession_no)
set_of_edgar_filing_accession_no = set()
for row in edgar_filing_accession_no_results:
    for edgar_filing_accession_no in row:
        set_of_edgar_filing_accession_no.add(edgar_filing_accession_no)

difference = set_of_edgar_filing_accession_no.difference(set_of_data13f_accession_no)
print("# of filings with missing data: ", len(difference))

for accession_no in difference:
    dates_with_missing_data = EdgarFiling.query.filter(EdgarFiling.accession_no == accession_no).first()
    db.session.delete(dates_with_missing_data)
    db.session.commit()
    print("deleted edgarfiling")
