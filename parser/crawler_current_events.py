"""module docstring"""
import re
import requests


def grab_text(url):
    getter = requests.get(url)
    full_text = getter.text
    return full_text


def get_13f_filing_detail_urls(edgar_current_events_text):
    base_sec_url = "https://www.sec.gov"
    url_list = []
    for suffix_url in re.findall('(?<=<a href=")(.*)(?=">13F)', edgar_current_events_text):
        url_list.append(base_sec_url + suffix_url)
    return url_list


def get_primary_doc_and_infotable_urls(text_13f):
    return re.findall('(?<=<a href=")(.*)(?=">.*.xml)', text_13f)


def get_primary_doc_xml_url(suffix_xml_urls):
    base_sec_url = "https://www.sec.gov"
    if suffix_xml_urls:
        return base_sec_url + suffix_xml_urls[0]
    raise TypeError("Can't find URL on current webpage")


def get_infotable_xml_url(partial_xml_url):
    base_sec_url = "https://www.sec.gov"
    if partial_xml_url:
        return base_sec_url + partial_xml_url[-1]
    raise TypeError("Can't find URL on current webpage")
