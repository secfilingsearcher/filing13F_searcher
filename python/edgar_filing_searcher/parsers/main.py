# pylint: disable=import-error
"""This file contains the main method"""
import logging

from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import Company, EdgarFiling
from edgar_filing_searcher.parsers.crawler_current_events import get_text, \
    parse_13f_filing_detail_urls
from edgar_filing_searcher.parsers.errors import CantFindUrlException
from edgar_filing_searcher.parsers.parser_class import Parser
from edgar_filing_searcher.parsers.setup_db_connection import setup_db_connection

URL_EDGAR_CURRENT_EVENTS = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=13f'


def create_url_list(url_edgar_current_events):
    """This function creates a list of URLs"""
    text_edgar_current_events = get_text(url_edgar_current_events)
    logging.info('Extracted URLs from %s', url_edgar_current_events)
    return parse_13f_filing_detail_urls(text_edgar_current_events)


def update_filing_counts(cik_no_list):
    """This function counts the number of filings and adds it to the Company table"""
    for cik_no in cik_no_list:
        company_in_table = Company.query.filter_by(cik_no=cik_no).first()
        filing_count = EdgarFiling.query.filter_by(cik_no=cik_no).count()
        company_in_table.filing_count = filing_count
        logging.debug('Counted amount of filings for CIK: %s. Count: %i', cik_no, filing_count)
        db.session.commit()
        logging.info('Added number of filings for CIK: %s to Company table', cik_no)


def send_data_to_db(company_row, edgar_filing_row, data_13f_table):
    """This function sends data to the database"""
    db.session.merge(company_row)
    db.session.merge(edgar_filing_row)
    for data_13f_row in data_13f_table:
        db.session.merge(data_13f_row)
        logging.debug('Data_13f_row session merged %s', data_13f_row)
    db.session.commit()
    logging.info('Sent company_row, edgar_filing_row, data_13f_table data to Database')


def main():
    """This function returns the cik, company name, and infotable data"""
    logging.basicConfig(format='%(asctime)s, %(filename)s, %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    logging.info('Initializing job')
    filing_detail_urls = create_url_list(URL_EDGAR_CURRENT_EVENTS)
    if not filing_detail_urls:
        raise CantFindUrlException("There are no urls on the page")
    setup_db_connection()
    list_of_cik_no = []
    for filing_detail_url in filing_detail_urls:
        parser = Parser(filing_detail_url)
        list_of_cik_no.append(parser.company.cik_no)
        send_data_to_db(
            parser.company,
            parser.edgar_filing,
            parser.data_13f)
    update_filing_counts(list_of_cik_no)


if __name__ == "__main__":
    main()
