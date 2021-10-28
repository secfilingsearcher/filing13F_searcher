"""Delete data13f data with missing edgarfiling"""
from models import EdgarFiling, Data13f
from parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.database import db

setup_db_connection()

edgar_filing_accession_no_results = EdgarFiling.query.with_entities(
    EdgarFiling.accession_no).group_by(
    EdgarFiling.accession_no).all()

missing_edgarfiling_accession_numbers = []
for row in edgar_filing_accession_no_results:
    for edgar_filing_accession_no in row:
        if not Data13f.query.filter(Data13f.accession_no == edgar_filing_accession_no).first():
            missing_edgarfiling_accession_numbers.append(edgar_filing_accession_no)

print("# of missing filings: ", len(missing_edgarfiling_accession_numbers))

# for accession_no in missing_edgarfiling_accession_numbers:
#     dates_with_missing_data = Data13f.query.filter(Data13f.accession_no == accession_no).all()
#     for row in dates_with_missing_data:
#         db.session.delete(row)
#         db.session.commit()
#         print("del one of all")

# for accession_no in missing_edgarfiling_accession_numbers:
#     dates_with_missing_data = Data13f.query.filter(Data13f.accession_no == accession_no).delete()
#     db.session.commit()
#     print("del all query")
