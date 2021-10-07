"""This file crawls from the current events EDGAR page to the primary_doc and infotable xml file"""
import logging
import re
import time
from datetime import date, timedelta

import requests


def get_text(url):
    """Returns the html and text from the url"""
    response = requests.get(
        url,
        headers={"user-agent": "filing_13f_searcher"}
    )
    if response.status_code != 200:
        logging.warning("get_text, Unexpected status code %s", response.status_code)
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
        search_url = base_url + "/" + f'{full_date.year}' + "/" + \
                     f'QTR{quarter}' + "/" + f'company.{subdirectory_date_94}.idx'
    elif 1995 <= full_date.year <= 1997:
        search_url = base_url + "/" + f'{full_date.year}' + "/" + \
                     f'QTR{quarter}' + "/" + f'company.{subdirectory_date_95_97}.idx'
    else:
        search_url = base_url + "/" + f'{full_date.year}' + "/" + \
                     f'QTR{quarter}' + "/" + f'company.{subdirectory_date_after_1998}.idx'

    response = requests.get(
        search_url,
        headers={"User-Agent": "filing_13f_searcher"}
    )
    if response.status_code != 200:
        logging.warning("get_subdirectories_for_specific_date, Unexpected status code %s",
                        response.status_code)
    time.sleep(1)
    full_text = response.text

    all_13f_filings = re.findall('(?<=13F-HR)(.*)(?=.txt)', full_text, flags=re.IGNORECASE)
    if not all_13f_filings:
        return None
    return [re.search(r'(?<=edgar/data/)(.*)', x).group(0) for x in all_13f_filings]


def ensure_13f_filing_detail_urls(cik_ascension_subdirectories):
    """Returns the 13f filing detail url"""
    specific_date_13f_filing_detail_urls = \
        ["https://www.sec.gov/Archives/edgar/data/" + subdirectory +
         "-index.html" for subdirectory in cik_ascension_subdirectories]
    return specific_date_13f_filing_detail_urls


def generate_dates(start_date: date, end_date: date):
    """This function iterates over a range of dates"""
    delta = timedelta(days=1)

    while start_date <= end_date:
        yield start_date
        start_date += delta
