# pylint: disable=import-error
"""This file contains the main method"""
import argparse
import logging
import sys
import traceback
from datetime import date

from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import Company, EdgarFiling, Data13f
from edgar_filing_searcher.parsers.daily_index_crawler import \
    ensure_13f_filing_detail_urls, generate_dates, get_subdirectories_for_specific_date
from edgar_filing_searcher.parsers.parser_class import Parser
from edgar_filing_searcher.parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.errors import BadWebPageResponseException, NoUrlException, \
    NoAccessionNumberException, InvalidUrlException


def create_url_list(date_):
    """This function creates a list of 13F URLs"""
    subdirectories = get_subdirectories_for_specific_date(date_)
    if not subdirectories:
        logging.info('No cik_no_and_accession_nos for date: %s', date_)
        return None
    logging.info('Extracted cik_no_and_accession_nos for date: %s', date_)
    return ensure_13f_filing_detail_urls(subdirectories)


def check_parser_values_align(company: Company, edgar_filing: EdgarFiling, data_13f: Data13f):
    """check_ if the parser values from Company, EdgarFiling,
    Data13f CIK number and accession number align"""
    return (company.cik_no == edgar_filing.cik_no) and \
           (edgar_filing.accession_no == data_13f[0].accession_no)


def check_if_filing_exists_in_db(accession_no):
    """Check if the filing exists in the database"""
    return bool(EdgarFiling.query.filter_by(accession_no=accession_no).first())


def update_filing_count(parser: Parser):
    """This function counts the number of filings and adds it to the Company table"""
    cik_no = parser.edgar_filing.cik_no
    accession_no = parser.edgar_filing.accession_no
    current_db_filing_count = EdgarFiling.query.filter_by(cik_no=cik_no).count()
    logging.debug('Counted number of filings for CIK: %s. Count: %i',
                  cik_no, current_db_filing_count)
    if check_if_filing_exists_in_db(accession_no):
        logging.debug('Maintain same number of filings %i for CIK: %s.',
                      current_db_filing_count, cik_no)
        parser.company.filing_count = current_db_filing_count
    else:
        parser.company.filing_count = 1 + current_db_filing_count
        logging.debug('Number of filings change from %i to %i for CIK: %s',
                      current_db_filing_count, parser.company.filing_count, cik_no)
    logging.info('Updated number of filings for CIK: %s to Company table', cik_no)


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


def _process_date(date_):
    try:
        filing_detail_urls = create_url_list(date_)
    except InvalidUrlException:
        logging.info("There is an invalid daily filings URL for date %s", date_)
        return
    except BadWebPageResponseException:
        logging.info("There is no data returned from the page for date %s", date_)
        return
    if not filing_detail_urls:
        logging.info("There are no filing URLs on the filing detail page for date %s", date_)
        return
    for filing_detail_url in filing_detail_urls:
        _process_filing_detail_url(filing_detail_url)


def _process_filing_detail_url(filing_detail_url):
    try:
        parser = Parser(filing_detail_url)
    except NoUrlException:
        logging.error("There is no XML URL on the filing detail page: %s",
                      filing_detail_url)
        return
    except NoAccessionNumberException:
        logging.error("There is no accession no on the filing detail page: %s",
                      filing_detail_url)
        return
    if check_parser_values_align(parser.company, parser.edgar_filing, parser.data_13f):
        update_filing_count(parser)
        send_data_to_db(
            parser.company,
            parser.edgar_filing,
            parser.data_13f)
    else:
        logging.error("CIK and Accession_no do not match. Data not sent to database.")


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

    setup_db_connection()
    for date_ in generate_dates(start_date, end_date):
        _process_date(date_)


if __name__ == "__main__":
    main()
