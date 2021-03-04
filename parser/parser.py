import requests
import re

url_edgar_current_events = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'
getter = requests.get(url_edgar_current_events)
text_edgar_current_events = getter.text

primary_doc_xml_list = []
infotable_xml_list = []

for partial_url_13f_hr in re.findall('(?<=<a href=")(.*)(?=">13F-HR</a>)', text_edgar_current_events, flags=0):
    front_sec_url = "https://www.sec.gov"
    full_url_13f_hr = front_sec_url + partial_url_13f_hr
    getter = requests.get(full_url_13f_hr)
    text_13f_hr = getter.text
    # grab link 1
    partial_primary_doc_xml_url = re.search('(?<=<a href=")(.*)(?=">primary_doc.html)', text_13f_hr, flags=0)
    if partial_primary_doc_xml_url:
        partial_primary_doc_xml_url = partial_primary_doc_xml_url.group(0)
        full_primary_doc_xml_url = front_sec_url + partial_primary_doc_xml_url
        primary_doc_xml_list.append(full_primary_doc_xml_url)
    else:
        # need to return error
        print('None')
    # grab link 2
    partial_infotable_xml_url = re.search('(?<=<a href=")(.*)(?=">infotable.html)', text_13f_hr, flags=0)
    if partial_infotable_xml_url:
        partial_infotable_xml_url = partial_infotable_xml_url.group(0)
        full_infotable_xml_url = front_sec_url + partial_infotable_xml_url
        infotable_xml_list.append(full_infotable_xml_url)
    else:
        # need to return error
        print('None')
    break

print(primary_doc_xml_list)
print(infotable_xml_list)