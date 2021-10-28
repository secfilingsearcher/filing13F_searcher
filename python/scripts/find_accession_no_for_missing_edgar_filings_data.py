"""Checks for missing edgarfiling data and prints date and accession_no"""
from models import EdgarFiling, Data13f
from parsers.setup_db_connection import setup_db_connection

setup_db_connection()

edgar_filing_accession_no_results = EdgarFiling.query.with_entities(
    EdgarFiling.accession_no).group_by(
    EdgarFiling.accession_no).all()

missing_edgarfiling_accession_no = []
for row in edgar_filing_accession_no_results:
    for edgar_filing_accession_no in row:
        if not Data13f.query.filter(Data13f.accession_no == edgar_filing_accession_no).first():
            missing_edgarfiling_accession_no.append(edgar_filing_accession_no)

print(missing_edgarfiling_accession_no)
