# pylint: disable=import-error
"""This file contains the main method"""
import argparse
import logging
import sys
import traceback
from datetime import datetime

from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import Company, EdgarFiling
from edgar_filing_searcher.parsers.crawler_current_events import \
    ensure_13f_filing_detail_urls, generate_dates, get_specific_date_cik_no_and_accession_no
from edgar_filing_searcher.parsers.parser_class import Parser
from edgar_filing_searcher.parsers.setup_db_connection import setup_db_connection
from errors import InvalidDate

URL_EDGAR_CURRENT_EVENTS = 'https://www.sec.gov/Archives/edgar/full-index/'


def create_url_list(date_):
    """This function creates a list of URLs"""
    cik_no_and_accession_nos = get_specific_date_cik_no_and_accession_no(date_)
    logging.info('Extracted cik_no_and_accession_nos from %s', cik_no_and_accession_nos)
    return ensure_13f_filing_detail_urls(cik_no_and_accession_nos)


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


def my_handler(exc_type, exc_value, exc_traceback):
    """Log uncaught exceptions with logger."""
    logging.exception("Uncaught exception: %s",
                      ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))


def change_sys_excepthook():
    """Setup an exception handler to log uncaught exceptions."""
    sys.excepthook = my_handler


def main():
    """This function returns the cik, company name, and infotable data"""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--start_date", help="Beginning date",
                            type=datetime, default=datetime.today())
    arg_parser.add_argument("--end_date", help="End date",
                            type=datetime, default=datetime.today())
    args = arg_parser.parse_args()

    start_date = args.start_date
    end_date = args.end_date

    logging.basicConfig(format='%(asctime)s, %(filename)s, %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

    change_sys_excepthook()

    logging.info('Initializing job')

    for date_ in generate_dates(start_date, end_date):
        filing_detail_urls = create_url_list(date_)
        if not filing_detail_urls:
            logging.info("There are no urls on the Edgar Daily Index page")
            sys.exit(0)
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
