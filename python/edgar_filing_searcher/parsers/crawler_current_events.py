"""This file crawls from the current events EDGAR page to the primary_doc and infotable xml file"""
import logging
import re
import sys
import time
from datetime import date, timedelta

import requests

from edgar_filing_searcher.errors import NoUrlException, InvalidDate


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


def parse_13f_filing_detail_urls(edgar_current_events_text):
    """Returns the 13f filing detail base urls"""
    filing_detail_url_suffixes = re.findall('(?<=<a href=")(.*)(?=">13F)',
                                            edgar_current_events_text)
    if not filing_detail_url_suffixes:
        raise NoUrlException()
    return filing_detail_url_suffixes


def get_cik_no_and_accession_no_for_specific_date(full_date: date):
    """Returns the cik no and accession no for a specific date"""
    quarter = (full_date.month // 4) + 1
    short = full_date.strftime('%Y%m%d')

    base_url = "https://www.sec.gov/Archives/edgar/daily-index"
    search_url = base_url + "/" + f'{full_date.year}' + "/" + f'QTR{quarter}' + "/" \
                 + f'company.{short}.idx'

    response = requests.get(
        search_url,
        headers={"user-agent": "filing_13f_searcher"}
    )
    if response.status_code != 200:
        logging.warning("Unexpected status code %s", response.status_code)

    time.sleep(1)
    full_text = response.text

    return re.findall('(?<=edgar/data/)(.*)(?=.txt)', full_text, flags=re.IGNORECASE)


def ensure_13f_filing_detail_urls(date_filing_detail_url_cik_no_and_accession_nos):
    """Returns the 13f filing detail url"""
    specific_date_filing_detail_url_list = []
    try:
        for cik_no_and_accession_no in date_filing_detail_url_cik_no_and_accession_nos:
            specific_date_filing_detail_url_list.append(
                "https://www.sec.gov/Archives/edgar/data/" + cik_no_and_accession_no + "-index.html")
    except NoUrlException:
        logging.critical("Found no 13f cik_no_and_accession_no.")
        sys.exit(-1)
    return specific_date_filing_detail_url_list


def generate_dates(start_date: date, end_date: date):
    """Returns the html and text from the url"""
    delta = timedelta(days=1)

    while start_date <= end_date:
        yield start_date
        start_date += delta
