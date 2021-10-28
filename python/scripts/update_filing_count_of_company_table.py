"""Checks the filing count and updates the filing count in the edgar_filing table"""
from models import Company, EdgarFiling
from parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.database import db

setup_db_connection()

count_of_companies_with_zero_filing_count = Company.query.filter_by(filing_count=0).count()

if count_of_companies_with_zero_filing_count > 0:
    print("Companies where filing count is 0:", count_of_companies_with_zero_filing_count)
    Companies_with_zero_filing_count = db.session.query(
        Company).filter(Company.filing_count == 0).all()
    for company in Companies_with_zero_filing_count:
        check_actual_filing_count_in_edgarfiling_table = db.session.query(EdgarFiling).filter(
            EdgarFiling.cik_no == company.cik_no).count()
        company.filing_count = check_actual_filing_count_in_edgarfiling_table
        db.session.merge(company)
        db.session.commit()
