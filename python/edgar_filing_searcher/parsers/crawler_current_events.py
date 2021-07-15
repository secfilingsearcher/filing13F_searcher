"""This file crawls from the current events EDGAR page to the primary_doc and infotable xml file"""
import logging
import re
import time

import requests

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
    """Returns the 13f filing detail url"""
    base_sec_url = "https://www.sec.gov"
    url_list = []
    for suffix_url in re.findall('(?<=<a href=")(.*)(?=">13F)', edgar_current_events_text):
        url_list.append(base_sec_url + suffix_url)
    return url_list
