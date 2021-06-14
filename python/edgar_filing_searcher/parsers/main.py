# pylint: disable=import-error
"""This file contains the main method"""
from edgar_filing_searcher.database import db
from edgar_filing_searcher.parsers.crawler_current_events import get_text, \
    parse_13f_filing_detail_urls
from edgar_filing_searcher.parsers.parser_class import Parser
from edgar_filing_searcher.parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.models import Company, EdgarFiling

URL_EDGAR_CURRENT_EVENTS = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=13f'


def create_url_list(url_edgar_current_events):
    """This function creates a list of URLs"""
    text_edgar_current_events = get_text(url_edgar_current_events)
    return parse_13f_filing_detail_urls(text_edgar_current_events)


def send_data_to_db(company_row, edgar_filing_row, data_13f_table):
    """This function sends data to the database"""
    company_from_database = Company.query.filter_by(cik_no=company_row.cik_no).first()
    filing_from_database = EdgarFiling.query.filter_by(accession_no=edgar_filing_row.accession_no).first()
    if not filing_from_database and not company_from_database:
        company_row.filing_count = 1
    if not filing_from_database:
        company_row.filing_count = company_from_database.filing_count + 1
    else:
        company_row.filing_count = company_from_database.filing_count
    print(company_row.filing_count, "check")

    db.session.merge(company_row)
    db.session.merge(edgar_filing_row)
    for data_13f_row in data_13f_table:
        db.session.merge(data_13f_row)
    db.session.commit()


def main():
    """This function returns the cik, company name, and infotable data"""
    filing_detail_urls = create_url_list(URL_EDGAR_CURRENT_EVENTS)

    if not filing_detail_urls:
        print("There are no urls on the page")
        return

    for filing_detail_url in filing_detail_urls:
        setup_db_connection()
        parser = Parser(filing_detail_url)
        send_data_to_db(
            parser.company,
            parser.edgar_filing,
            parser.data_13f)

if __name__ == "__main__":
    main()
