"""Checks for missing Data13f and EdgarFiling data and prints dates and accession numbers"""
from models import EdgarFiling, Data13f
from parsers.setup_db_connection import setup_db_connection

setup_db_connection()

all_edgar_filing_accession_no = EdgarFiling.query.with_entities(
    EdgarFiling.accession_no).group_by(
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

edgarfiling_accession_no_with_missing_data13f_data = \
    set_of_edgar_filing_accession_no.difference(set_of_data13f_accession_no)

unique_dates_with_missing_data = set()
accession_nos_and_dates_with_missing_data = []
for accession_no in edgarfiling_accession_no_with_missing_data13f_data:
    all_dates = EdgarFiling.query.with_entities(EdgarFiling.filing_date).group_by(
        EdgarFiling.filing_date).filter(EdgarFiling.accession_no == accession_no).all()
    for row in all_dates:
        for date in row:
            unique_dates_with_missing_data.add(date)
            accession_nos_and_dates_with_missing_data.append((date, accession_no))

sorted_dates = sorted(unique_dates_with_missing_data)
print("Number data13f rows with missing data:", len(sorted_dates))
print("Dates with missing data: ")
for dates in sorted_dates:
    print(dates.strftime("%B %d,%Y"))
print("\n")

sorted_dates_and_accession_no = sorted(accession_nos_and_dates_with_missing_data)
print("Number data13f rows with missing data:", len(sorted_dates_and_accession_no))
print("Dates and accession_no with missing data: ")
for dates_and_accession_no in sorted_dates_and_accession_no:
    print(f"{dates_and_accession_no[0].strftime('%Y-%m-%d')}: {dates_and_accession_no[1]}")
