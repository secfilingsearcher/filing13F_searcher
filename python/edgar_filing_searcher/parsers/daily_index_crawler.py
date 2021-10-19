# pylint: disable=no-member
"""This file crawls the daily index directory pages"""
import logging
import re
import time
from datetime import date, timedelta

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from edgar_filing_searcher.errors import BadWebPageResponseException, InvalidUrlException

BACKOFF_FACTOR_VALUE = 3
TIMEOUT_VALUE = 3


def get_request_response(url):
    """Returns the response request from the URL"""

    retry_strategy = Retry(
        total=3,
        status_forcelist=(403, 429, 500, 502, 503, 504),
        allowed_methods=["GET"],
        backoff_factor=BACKOFF_FACTOR_VALUE,
    )

    session = requests.Session()

    session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    response = session.get(
        url,
        headers={"user-agent": "filing_13f_searcher"}, timeout=TIMEOUT_VALUE
    )
    return response


def get_text(url):
    """Returns the html and text from the URL"""
    response = get_request_response(url)
    time.sleep(1)
    full_text = response.text
    logging.debug('Successfully ran get_text on URL %s', url)
    return full_text


def get_subdirectories_for_specific_date(full_date: date):
    """Returns all cik number and accession number subdirectory strings for a specific date"""
    base_url = "https://www.sec.gov/Archives/edgar/daily-index"
    quarter = round((full_date.month / 4) + 1)

    if full_date.year == 1994:
        subdirectory_date_94 = full_date.strftime('%m%d%y')
        full_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                   f'{subdirectory_date_94}.idx'

    elif 1995 <= full_date.year <= 1997:
        subdirectory_date_95_97 = full_date.strftime('%y%m%d')
        full_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                   f'{subdirectory_date_95_97}.idx'

    else:
        subdirectory_date_after_1998 = full_date.strftime('%Y%m%d')
        full_url = f'{base_url}/{full_date.year}/QTR{quarter}/company.' \
                   f'{subdirectory_date_after_1998}.idx'

    try:
        full_text = get_text(full_url)
    except requests.exceptions.RetryError as e:
        error_reason = str(e.args[0].reason)
        status_code = int((re.search('[0-9]+', error_reason))[0])
        logging.error('Response Status Code %i', status_code)
        if status_code in (403, 404):
            raise InvalidUrlException("Invalid URL error", status_code) from e
        raise BadWebPageResponseException("Web Page response error", status_code) from e

    split_full_text = full_text.splitlines()
    return [(re.search(r'(?<=edgar/data/)(.*)(?=.txt)', filing).group(0))
            for filing in split_full_text if filing[62:74].strip() == '13F-HR']


def ensure_13f_filing_detail_urls(cik_ascension_subdirectories):
    """Returns the 13f filing detail URL"""
    return [f'https://www.sec.gov/Archives/edgar/data/{subdirectory}-index.html'
            for subdirectory in cik_ascension_subdirectories]


def generate_dates(start_date: date, end_date: date):
    """This function iterates over a range of dates"""
    delta = timedelta(days=1)

    while start_date <= end_date:
        yield start_date
        start_date += delta
