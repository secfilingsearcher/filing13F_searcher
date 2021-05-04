# pylint: disable=import-error
"""This file contains the main method"""
from edgar_filing_searcher.parsers.main_functions import create_url_list, send_data_to_db
from edgar_filing_searcher.parsers.setup_db_connection import setup_db_connection
from edgar_filing_searcher.parsers.main_classes import Parser

URL_EDGAR_CURRENT_EVENTS = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=13f'


def main():
    """This function returns the cik, company name, and infotable data"""
    filing_detail_urls = create_url_list(URL_EDGAR_CURRENT_EVENTS)

    if not filing_detail_urls:
        print("There are no urls on the page")
        return

    for filing_detail_url in filing_detail_urls:
        setup_db_connection()
        send_data_to_db(
            Parser(filing_detail_url).company,
            Parser(filing_detail_url).edgar_filing,
            Parser(filing_detail_url).data_13f)


if __name__ == "__main__":
    main()
