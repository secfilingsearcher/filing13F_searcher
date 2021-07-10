# pylint: disable=import-error
"""This file contains the main method"""
import logging
from edgar_filing_searcher.database import db
from edgar_filing_searcher.parsers.crawler_current_events import get_text, \
    parse_13f_filing_detail_urls
from edgar_filing_searcher.parsers.parser_class import Parser
from edgar_filing_searcher.parsers.setup_db_connection import setup_db_connection
from parsers.errors import CantFindUrlException

URL_EDGAR_CURRENT_EVENTS = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=13f'


def create_url_list(url_edgar_current_events):
    """This function creates a list of URLs"""
    logging.info('parsers.main.py: Start running get_text on url_edgar_current_events')
    text_edgar_current_events = get_text(url_edgar_current_events)
    logging.info('parsers.main.py: Ran get_text on url_edgar_current_events')
    return parse_13f_filing_detail_urls(text_edgar_current_events)


def send_data_to_db(company_row, edgar_filing_row, data_13f_table):
    """This function sends data to the database"""
    logging.info('parsers.main.py: Start merge on company_row session ')
    db.session.merge(company_row)
    logging.info('parsers.main.py: Company row session merged')
    logging.info('parsers.main.py: Start merge on edgar filing row')
    db.session.merge(edgar_filing_row)
    logging.info('parsers.main.py: Edgar filing row session merged')
    for data_13f_row in data_13f_table:
        logging.info('parsers.main.py: Start merge on data 13f row')
        db.session.merge(data_13f_row)
        logging.info('parsers.main.py: Data 13f row session merged')
    logging.info('parsers.main.py: Start session commit')
    db.session.commit()
    logging.info('parsers.main.py: Session committed')


def main():
    """This function returns the cik, company name, and infotable data"""
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    filing_detail_urls = create_url_list(URL_EDGAR_CURRENT_EVENTS)

    if not filing_detail_urls:
        raise CantFindUrlException("There are no urls on the page")

    logging.info('parsers.main.py: Start database connection')
    setup_db_connection()
    logging.info('parsers.main.py: Database connection set up')
    for filing_detail_url in filing_detail_urls:
        logging.info('parsers.main.py: Start initializing parser')
        parser = Parser(filing_detail_url)
        logging.info('parsers.main.py: Parser initialized')
        logging.info('parsers.main.py: Start sending parser with send_data_to_db')
        send_data_to_db(
            parser.company,
            parser.edgar_filing,
            parser.data_13f)
        logging.info('parsers.main.py: Sent parser with send_data_to_db')


if __name__ == "__main__":
    main()
