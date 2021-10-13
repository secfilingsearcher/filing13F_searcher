# pylint: disable=invalid-name
"""This file crawls from the current events EDGAR page to the primary_doc and infotable xml file"""
import logging
import re
import time
from datetime import date, timedelta

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from edgar_filing_searcher.errors import BadWebPageException


def get_request_response(url):
    """Returns the response request from the url"""
    retry_strategy = Retry(
        total=3,
        status_forcelist=(403, 429, 500, 502, 503, 504),
        allowed_methods=["GET"],
        backoff_factor=3,
    )

    session = requests.Session()

    session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    response = session.get(
        url,
        headers={"user-agent": "filing_13f_searcher"}, timeout=3
    )
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
        full_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                   f'{subdirectory_date_94}.idx'

    elif 1995 <= full_date.year <= 1997:
        full_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                   f'{subdirectory_date_95_97}.idx'

    else:
        full_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                   f'{subdirectory_date_after_1998}.idx'

    try:
        full_text = get_text(full_url)
    except requests.exceptions.RetryError as e:
        raise BadWebPageException("Search Page has error", e)

    all_13f_filings = re.findall('(?<=13F-HR)(.*)(?=.txt)', full_text, flags=re.IGNORECASE)
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
