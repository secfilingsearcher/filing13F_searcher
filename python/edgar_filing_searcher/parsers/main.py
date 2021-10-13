# pylint: disable=import-error
"""This file contains the main method"""
import argparse
import logging
import sys
import traceback
from datetime import date

from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import Company, EdgarFiling
from edgar_filing_searcher.parsers.daily_index_crawler import \
    ensure_13f_filing_detail_urls, generate_dates, get_subdirectories_for_specific_date
from edgar_filing_searcher.parsers.parser_class import Parser
from edgar_filing_searcher.parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.errors import BadWebPageException, UrlErrorException, NoAccessionNo


def create_url_list(date_):
    """This function creates a list of 13F URLs"""
    subdirectories = get_subdirectories_for_specific_date(date_)
    if not subdirectories:
        logging.info('No cik_no_and_accession_nos for date: %s', date_)
        return None
    logging.info('Extracted cik_no_and_accession_nos for date: %s', date_)
    return ensure_13f_filing_detail_urls(subdirectories)


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
                            type=date.fromisoformat, default=date.today())
    arg_parser.add_argument("--end_date", help="End date",
                            type=date.fromisoformat, default=date.today())
    args = arg_parser.parse_args()

    start_date = args.start_date
    end_date = args.end_date

    logging.basicConfig(format='%(levelname)s: %(asctime)s-- %(pathname)s,'
                               ' line %(lineno)d, in %(module)s, %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

    change_sys_excepthook()

    logging.info('Initializing job')

    for date_ in generate_dates(start_date, end_date):
        try:
            filing_detail_urls = create_url_list(date_)
        except BadWebPageException:
            logging.info("There are no filing urls on the page for date %s", date_)
            continue
        setup_db_connection()
        list_of_cik_no = []
        for filing_detail_url in filing_detail_urls:
            try:
                parser = Parser(filing_detail_url)
            except (UrlErrorException, NoAccessionNo):
                logging.info("There is no URL for filing_detail_url: %s", filing_detail_url)
                continue
            list_of_cik_no.append(parser.company.cik_no)
            send_data_to_db(
                parser.company,
                parser.edgar_filing,
                parser.data_13f)
        update_filing_counts(list_of_cik_no)


if __name__ == "__main__":
    main()
