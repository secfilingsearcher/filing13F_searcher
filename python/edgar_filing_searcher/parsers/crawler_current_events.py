"""This file crawls from the current events EDGAR page to the primary_doc and infotable xml file"""
import logging
import re
import time
import requests

from edgar_filing_searcher.parsers.errors import CantFindUrlException


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
    try:
        filing_detail_url_suffixes
    except CantFindUrlException:
        logging.exception("13f filing detail url suffix is empty.")
    return filing_detail_url_suffixes


def ensure_13f_filing_detail_urls(edgar_current_events_text):
    """Returns the 13f filing detail url"""
    sec_base_url = "https://www.sec.gov"
    url_list = []
    for filing_detail_url_suffix in parse_13f_filing_detail_urls(edgar_current_events_text):
        url_list.append(sec_base_url + filing_detail_url_suffix)
    return url_list
