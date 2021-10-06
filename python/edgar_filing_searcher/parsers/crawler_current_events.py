"""This file crawls from the current events EDGAR page to the primary_doc and infotable xml file"""
import logging
import re
import sys
import time
from datetime import date, timedelta

import requests

from edgar_filing_searcher.errors import NoUrlException


def get_text(url):
    """Returns the html and text from the url"""
    response = requests.get(
        url,
        headers={"user-agent": "filing_13f_searcher"}
    )
    if response.status_code != 200:
        logging.warning("Unexpected status code %s", response.status_code)
    time.sleep(1)
    full_text = response.text
    logging.debug('Successfully ran get_text on url %s', url)
    return full_text


def get_subdirectories_for_specific_date(full_date: date):
    """Returns all cik number and accession number subdirectory strings for a specific date"""
    quarter = (full_date.month // 4) + 1
    short = full_date.strftime('%Y%m%d')

    base_url = "https://www.sec.gov/Archives/edgar/daily-index"
    search_url = base_url + "/" + f'{full_date.year}' + "/" + \
                 f'QTR{quarter}' + "/" + f'company.{short}.idx'
    response = requests.get(
        search_url,
        headers={"User-Agent": "filing_13f_searcher"}
    )
    if response.status_code != 200:
        logging.warning("Unexpected status code %s", response.status_code)
    time.sleep(1)
    full_text = response.text

    all_13f_filings = re.findall('(?<=13F)(.*)(?=.txt)', full_text, flags=re.IGNORECASE)
    if not all_13f_filings:
        return None
    return [re.search(r'(?<=edgar/data/)(.*)', x).group(0) for x in all_13f_filings]


def ensure_13f_filing_detail_urls(cik_ascension_subdirectories):
    """Returns the 13f filing detail url"""
    specific_date_13f_filing_detail_urls = []
    try:
        for subdirectory in cik_ascension_subdirectories:
            specific_date_13f_filing_detail_urls.append(
                "https://www.sec.gov/Archives/edgar/data/" +
                subdirectory + "-index.html")
    except NoUrlException:
        logging.critical("Found no 13f cik_no_and_accession_no.")
        sys.exit(-1)
    return specific_date_13f_filing_detail_urls


def generate_dates(start_date: date, end_date: date):
    """This function iterates over a range of dates"""
    delta = timedelta(days=1)

    while start_date <= end_date:
        yield start_date
        start_date += delta
