"""Checks for mismatched in edgarfiling and data13f and prints data"""
from models import EdgarFiling, Data13f
from parsers.setup_db_connection import setup_db_connection

setup_db_connection()

edgar_filing_accession_no_results = EdgarFiling.query.with_entities(
    EdgarFiling.accession_no).group_by(
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

set_of_dates_with_missing_data = set()
for accession_no in difference:
    dates_with_missing_data = EdgarFiling.query.with_entities(EdgarFiling.filing_date).group_by(
        EdgarFiling.filing_date).filter(EdgarFiling.accession_no == accession_no).all()
    for row in dates_with_missing_data:
        for date in row:
            set_of_dates_with_missing_data.add(date)

sorted_dates_with_missing_data = sorted(set_of_dates_with_missing_data)
print("Dates with missing data: ")
for dates_with_missing_data in sorted_dates_with_missing_data:
    print(dates_with_missing_data.strftime("%B %d,%Y"),
          " -> ",
          dates_with_missing_data.strftime("%Y-%m-%d"))
print("\n")

list_of_dates_and_accession_no_with_missing_data = []
for accession_no in difference:
    dates_with_missing_data = EdgarFiling.query.with_entities(EdgarFiling.filing_date).group_by(
        EdgarFiling.filing_date).filter(EdgarFiling.accession_no == accession_no).all()
    for row in dates_with_missing_data:
        for date in row:
            list_of_dates_and_accession_no_with_missing_data.append([date, accession_no])

sorted_list_of_dates_with_missing_data = sorted(list_of_dates_and_accession_no_with_missing_data)
print("Dates and accession_no with missing data: ")
for dates_with_missing_data in sorted_list_of_dates_with_missing_data:
    print(dates_with_missing_data[0].strftime("%B %d,%Y"),
          " -> ",
          dates_with_missing_data[0].strftime("%Y-%m-%d"),
          ": ",
          dates_with_missing_data[1])
print("\n")

print("Number of rows in data13f with missing data:",
      len(sorted_list_of_dates_with_missing_data))
