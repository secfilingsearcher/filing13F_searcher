import logging

from errors import InvalidUrlException, BadWebPageResponseException, NoUrlException, \
    NoAccessionNumberException
from edgar_filing_searcher.parsers.main import create_url_list, check_parser_values_align, \
    update_filing_count, \
    send_data_to_db
from edgar_filing_searcher.parsers.parser_class import Parser


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
