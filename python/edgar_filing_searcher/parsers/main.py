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
    logging.info('start running get_text on url_edgar_current_events')
    text_edgar_current_events = get_text(url_edgar_current_events)
    logging.info('ran get_text on url_edgar_current_events')
    return parse_13f_filing_detail_urls(text_edgar_current_events)


def send_data_to_db(company_row, edgar_filing_row, data_13f_table):
    """This function sends data to the database"""
    logging.info('start merge on company_row session ')
    db.session.merge(company_row)
    logging.info('company_row session merged')
    logging.info('start merge on edgar_filing_row')
    db.session.merge(edgar_filing_row)
    logging.info('edgar_filing_row session merged')
    for data_13f_row in data_13f_table:
        logging.info('start merge on data_13f_row')
        db.session.merge(data_13f_row)
        logging.info('data_13f_row session merged')
    logging.info('start session commit')
    db.session.commit()
    logging.info('session committed')


def main():
    """This function returns the cik, company name, and infotable data"""
    filing_detail_urls = create_url_list(URL_EDGAR_CURRENT_EVENTS)

    if not filing_detail_urls:
        raise CantFindUrlException("There are no urls on the page")

    logging.info('start setup_db_connection')
    setup_db_connection()
    logging.info('db_connection set up')
    for filing_detail_url in filing_detail_urls:
        logging.info('start initializing parser')
        parser = Parser(filing_detail_url)
        logging.info('parser initialized')
        logging.info('start sending parser with send_data_to_db')
        send_data_to_db(
            parser.company,
            parser.edgar_filing,
            parser.data_13f)
        logging.info('sent parser with send_data_to_db')


if __name__ == "__main__":
    main()
