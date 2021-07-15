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
    """Returns the 13f filing detail url"""
    base_sec_url = "https://www.sec.gov"
    url_list = []
    for suffix_url in re.findall('(?<=<a href=")(.*)(?=">13F)', edgar_current_events_text):
        url_list.append(base_sec_url + suffix_url)
    return url_list


def parse_sec_accession_no(text_13f):
    """Returns the sec accession number from the 13f filing detail page"""
    return re \
        .search('(?<=Accession <acronym title="Number">No.</acronym></strong> )(.*)', text_13f) \
        .group(0)


def parse_primary_doc_xml_and_infotable_xml_urls(text_13f):
    """Returns the primary_doc.xml and infotable.xml base urls"""
    return re.findall('(?<=<a href=")(.*)(?=">.*.xml)', text_13f, flags=re.IGNORECASE)


def parse_primary_doc_xml_url(suffix_xml_urls):
    """Adds base url to suffix url for primary_doc.xml url"""
    base_sec_url = "https://www.sec.gov"
    if suffix_xml_urls:
        return base_sec_url + suffix_xml_urls[0]
    logging.critical("Primary_doc_xml_url suffix is empty.")
    raise CantFindUrlException()


def parse_infotable_xml_url(partial_xml_url):
    """Adds base url to suffix url for infotable.xml url"""
    base_sec_url = "https://www.sec.gov"
    if partial_xml_url:
        return base_sec_url + partial_xml_url[-1]
    logging.critical("Infotable_xml_url suffix is empty.")
    raise CantFindUrlException()
