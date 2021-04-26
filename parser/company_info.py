"""This file contains functions that parse primary_doc.xml"""
from models import Company


def get_primary_doc(accession_no_value, cik_value, company_name, filing_date):
    """Gets the data input as parameter from primary_doc.xml and 13f filing webpage
    and instantiates an object"""
    row = Company(accession_no=accession_no_value,
                  cik_no=cik_value,
                  company_name=company_name,
                  filing_date=filing_date)
    return row
