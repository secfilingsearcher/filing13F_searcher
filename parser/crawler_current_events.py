import requests
import re
from parser_13f_infotable import infotable_parser
from parser_13f_primary_doc import primary_doc_parser

edgar_13f_filing_detail_url_list = []
primary_doc_xml_list = []
infotable_xml_list = []


def crawl_page():
    url_edgar_current_events = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'
    getter = requests.get(url_edgar_current_events)
    text_edgar_current_events = getter.text

    for partial_url_13f_hr in re.findall('(?<=<a href=")(.*)(?=">13F)', text_edgar_current_events, flags=0):
        front_sec_url = "https://www.sec.gov"
        full_url_13f_hr = front_sec_url + partial_url_13f_hr
        getter = requests.get(full_url_13f_hr)
        text_13f_hr = getter.text
        # get filing detail_page
        edgar_13f_filing_detail_url_list.append(full_url_13f_hr)
        # grab link 1 + 2
        partial_infotable_xml_url = re.findall('(?<=<a href=")(.*)(?=">.*.xml)', text_13f_hr, flags=0)
        if partial_infotable_xml_url:
            full_infotable_xml_url = front_sec_url + partial_infotable_xml_url[0]
            full_infotable_xml_url = front_sec_url + partial_infotable_xml_url[-1]
            primary_doc_xml_list.append(full_infotable_xml_url)
            infotable_xml_list.append(full_infotable_xml_url)
        else:
            raise TypeError("Can't find URL on current webpage")


def main():
    crawl_page()
    # create for loop and use one row function to cik
    primary_doc_parser(primary_doc_xml_list[0])
    # print(primary_doc_xml_list[0])
    # print(infotable_xml_list[0])

    # create for loop and use infotable function to get database



if __name__ == "__main__":
    main()




print()
print("check")
print(edgar_13f_filing_detail_url_list)
print(primary_doc_xml_list)
print(infotable_xml_list)
