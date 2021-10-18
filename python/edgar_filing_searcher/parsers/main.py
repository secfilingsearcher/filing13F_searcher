# pylint: disable=import-error
"""This file contains the main method"""
import argparse
import logging
import sys
import traceback
from datetime import date

from edgar_filing_searcher.parsers.daily_index_crawler import generate_dates
from edgar_filing_searcher.parsers.setup_db_connection import setup_db_connection

from parsers.parser_utils import process_date


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

    setup_db_connection()
    for date_ in generate_dates(start_date, end_date):
        process_date(date_)


if __name__ == "__main__":
    main()
