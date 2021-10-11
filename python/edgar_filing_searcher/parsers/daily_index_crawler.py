"""This file crawls from the current events EDGAR page to the primary_doc and infotable xml file"""
import logging
import re
import time
from datetime import date, timedelta

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_request_response(url):
    retry_strategy = Retry(
        total=5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=["GET"],
        backoff_factor=6,
    )

    http_session = requests.Session()

    http_session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    http_session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    response = None
    try:
        response = http_session.get(
            url,
            headers={"user-agent": "filing_13f_searcher"}, timeout=3
        )
    except requests.exceptions.HTTPError as e:
        logging.error('http', exc_info=e)
    except requests.exceptions.ConnectionError as e:
        logging.error('connection', exc_info=e)
    except requests.exceptions.RetryError as e:
        logging.error('retry', exc_info=e)
    return response


def get_text(url):
    """Returns the html and text from the url"""
    response = get_request_response(url)
    time.sleep(1)
    full_text = response.text
    logging.debug('Successfully ran get_text on url %s', url)
    return full_text


def get_subdirectories_for_specific_date(full_date: date):
    """Returns all cik number and accession number subdirectory strings for a specific date"""
    base_url = "https://www.sec.gov/Archives/edgar/daily-index"
    quarter = round((full_date.month / 4) + 1)
    subdirectory_date_94 = full_date.strftime('%m%d%y')
    subdirectory_date_95_97 = full_date.strftime('%y%m%d')
    subdirectory_date_after_1998 = full_date.strftime('%Y%m%d')

    if full_date.year == 1994:
        search_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                     f'{subdirectory_date_94}.idx'

    elif 1995 <= full_date.year <= 1997:
        search_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                     f'{subdirectory_date_95_97}.idx'

    else:
        search_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                     f'{subdirectory_date_after_1998}.idx'

    text = get_text(search_url)

    all_13f_filings = re.findall('(?<=13F-HR)(.*)(?=.txt)', text, flags=re.IGNORECASE)
    if not all_13f_filings:
        return None
    return [re.search(r'(?<=edgar/data/)(.*)', x).group(0) for x in all_13f_filings]


def ensure_13f_filing_detail_urls(cik_ascension_subdirectories):
    """Returns the 13f filing detail url"""
    specific_date_13f_filing_detail_urls = \
        [f'https://www.sec.gov/Archives/edgar/data/{subdirectory}-index.html'
         for subdirectory in cik_ascension_subdirectories]
    return specific_date_13f_filing_detail_urls


def generate_dates(start_date: date, end_date: date):
    """This function iterates over a range of dates"""
    delta = timedelta(days=1)

    while start_date <= end_date:
        yield start_date
        start_date += delta
