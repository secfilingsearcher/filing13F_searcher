from models import Company
from parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.database import db

setup_db_connection()

count_of_companies_with_zero_filing_count = Company.query.filter_by(filing_count=0).count()

if count_of_companies_with_zero_filing_count > 0:
    print("Companies where filing count is 0:", count_of_companies_with_zero_filing_count)
    Companies_with_zero_filing_count = db.session.query(
        Company).filter(Company.filing_count == 0).all()
    for filing_count in Companies_with_zero_filing_count:
        company_with_zero_filing_count = db.session.query(Company).filter(
            Company.filing_count == 0).first()
        db.session.delete(company_with_zero_filing_count)
        db.session.commit()
