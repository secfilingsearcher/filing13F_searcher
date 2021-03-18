"""This file crawls from the current events EDGAR page to the primary_doc and infotable xml file"""
import re
import requests


def get_text(url):
    """Returns the html and text from the url"""
    getter = requests.get(url)
    full_text = getter.text
    return full_text


def get_13f_filing_detail_urls(edgar_current_events_text):
    """Returns the 13f filing detail url"""
    base_sec_url = "https://www.sec.gov"
    url_list = []
    for suffix_url in re.findall('(?<=<a href=")(.*)(?=">13F)', edgar_current_events_text):
        url_list.append(base_sec_url + suffix_url)
    return url_list


def extract_sec_accession_no(text_13f):
    """Returns the sec accession number from the 13f filing detail page"""
    accession_no_str = re \
        .search('(?<=Accession <acronym title="Number">No.</acronym></strong> )(.*)', text_13f) \
        .group(0)
    accession_no_removed_dashes = accession_no_str.replace('-', '')
    accession_no = int(accession_no_removed_dashes)
    return accession_no


def get_primary_doc_and_infotable_urls(text_13f):
    """Returns the primary_doc.xml and infotable.xml base urls"""
    return re.findall('(?<=<a href=")(.*)(?=">.*.xml)', text_13f)


def get_primary_doc_xml_url(suffix_xml_urls):
    """Adds base url to suffix url for primary_doc.xml url"""
    base_sec_url = "https://www.sec.gov"
    if suffix_xml_urls:
        return base_sec_url + suffix_xml_urls[0]
    raise TypeError("Can't find URL on current webpage")


def get_infotable_xml_url(partial_xml_url):
    """Adds base url to suffix url for infotable.xml url"""
    base_sec_url = "https://www.sec.gov"
    if partial_xml_url:
        return base_sec_url + partial_xml_url[-1]
    raise TypeError("Can't find URL on current webpage")
