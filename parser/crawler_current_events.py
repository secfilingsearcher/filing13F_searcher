import requests
import re


def grab_text(url):
    getter = requests.get(url)
    full_text = getter.text
    return full_text


def get_13f_filing_detail_urls_in_list(edgar_current_events_text, edgar_13f_filing_detail_url_list):
    prefix_sec_url = "https://www.sec.gov"
    for suffix_13f_filing_detail_url in re.findall('(?<=<a href=")(.*)(?=">13F)', edgar_current_events_text, flags=0):
        full_13f_filing_detail_url = prefix_sec_url + suffix_13f_filing_detail_url
        edgar_13f_filing_detail_url_list.append(full_13f_filing_detail_url)
    return edgar_13f_filing_detail_url_list

def get_primary_doc_and_infotable_urls(edgar_13f_filing_detail_text):
    suffix_all_xml_urls = re.findall('(?<=<a href=")(.*)(?=">.*.xml)', edgar_13f_filing_detail_text, flags=0)
    return suffix_all_xml_urls


def get_primary_doc_xml_urls_in_list(suffix_all_xml_urls, primary_doc_xml_list):
    prefix_sec_url = "https://www.sec.gov"
    if suffix_all_xml_urls:
        full_primary_doc_xml_url = prefix_sec_url + suffix_all_xml_urls[0]
        primary_doc_xml_list.append(full_primary_doc_xml_url)
    else:
        raise TypeError("Can't find URL on current webpage")


def get_infotable_xml_urls_in_list(partial_xml_url, infotable_xml_list):
    prefix_sec_url = "https://www.sec.gov"
    if partial_xml_url:
        full_infotable_xml_url = prefix_sec_url + partial_xml_url[-1]
        infotable_xml_list.append(full_infotable_xml_url)
    else:
        raise TypeError("Can't find URL on current webpage")

# def crawl_page_old(edgar_13f_filing_detail_url_list, primary_doc_xml_list, infotable_xml_list):
#     url_edgar_current_events = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'
#     getter = requests.get(url_edgar_current_events)
#     edgar_current_events_text = getter.text
#
#     for partial_url_13f_hr in re.findall('(?<=<a href=")(.*)(?=">13F)', edgar_current_events_text, flags=0):
#         prefix_sec_url = "https://www.sec.gov"
#         full_url_13f_hr = prefix_sec_url + partial_url_13f_hr
#         getter = requests.get(full_url_13f_hr)
#         text_13f_hr = getter.text
#         # get filing detail_page
#         edgar_13f_filing_detail_url_list.append(full_url_13f_hr)
#         # grab link 1 + 2
#         partial_xml_url = re.findall('(?<=<a href=")(.*)(?=">.*.xml)', text_13f_hr, flags=0)
#         if partial_xml_url:
#             full_primary_doc_xml_url = prefix_sec_url + partial_xml_url[0]
#             full_infotable_xml_url = prefix_sec_url + partial_xml_url[-1]
#             primary_doc_xml_list.append(full_primary_doc_xml_url)
#             infotable_xml_list.append(full_infotable_xml_url)
#         else:
#             raise TypeError("Can't find URL on current webpage")
