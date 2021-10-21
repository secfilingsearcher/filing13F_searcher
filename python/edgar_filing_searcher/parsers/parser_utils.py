"""This file contains functions used in main.py"""
import logging

from edgar_filing_searcher.database import db
from edgar_filing_searcher.models import Company, EdgarFiling, Data13f
from edgar_filing_searcher.parsers.daily_index_crawler import \
    ensure_13f_filing_detail_urls, get_subdirectories_for_specific_date
from edgar_filing_searcher.parsers.parser_class import Parser
from edgar_filing_searcher.errors import BadWebPageResponseException, NoUrlException, \
    NoAccessionNumberException, InvalidUrlException


def create_url_list(date_):
    """This function creates a list of 13F URLs"""
    subdirectories = get_subdirectories_for_specific_date(date_)
    if not subdirectories:
        logging.info('No CIK number and accession numbers for date %s', date_)
        return None
    logging.info('Extracted CIK number and accession numbers for date %s', date_)
    return ensure_13f_filing_detail_urls(subdirectories)


def check_parser_values_match(company: Company, edgar_filing: EdgarFiling, data_13f: Data13f):
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


def send_data_to_db(company_row: Company, edgar_filing_row: EdgarFiling, data_13f_table: [Data13f]):
    """This function sends data to the database"""
    db.session.merge(company_row)
    db.session.merge(edgar_filing_row)
    for data_13f_row in data_13f_table:
        db.session.merge(data_13f_row)
        logging.debug('Data_13f_row session merged %s', data_13f_row)
    db.session.commit()
    logging.info('Sent company row (CIK Number: %s), edgar filing row (Accession Number: %s), '
                 'and data 13f table data (%i rows) to Database',
                 company_row.cik_no, edgar_filing_row.accession_no, len(data_13f_table))


def process_date(date_):
    """This function process dates"""
    try:
        filing_detail_urls = create_url_list(date_)
    except InvalidUrlException as e:
        logging.warning("Response Status Code %i'. "
                        "There is an invalid daily filings URL for date %s", e.status_code, date_)
        return
    except BadWebPageResponseException as e:
        logging.warning("Response Status Code %i'. "
                        "There is no data returned from the page for date %s", e.status_code, date_)
        return
    if not filing_detail_urls:
        logging.info("There are no filing URLs on the filing detail page for date %s", date_)
        return
    for filing_detail_url in filing_detail_urls:
        process_filing_detail_url(filing_detail_url)


def process_filing_detail_url(filing_detail_url):
    """This function processes filing detail urls"""
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
    if check_parser_values_match(parser.company, parser.edgar_filing, parser.data_13f):
        update_filing_count(parser)
        send_data_to_db(
            parser.company,
            parser.edgar_filing,
            parser.data_13f)
    else:
        logging.error("CIK and Accession_no do not match. Data not sent to database.")
