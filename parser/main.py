import pandas as pd
from crawler_current_events import grab_text
from crawler_current_events import get_13f_filing_detail_urls_in_list
from crawler_current_events import get_primary_doc_and_infotable_urls
from crawler_current_events import get_primary_doc_xml_urls_in_list
from crawler_current_events import get_infotable_xml_urls_in_list
from parser_13f_primary_doc import primary_doc_parser
from parser_13f_infotable_V2 import infotable_parser

edgar_13f_list = []
primary_doc_list = []
infotable_list = []

# TODO; make function with no arg that returns lists that can be used outside


def main():
    url_edgar_current_events = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'
    text_edgar_current_events = grab_text(url_edgar_current_events)
    all_urls_13f = get_13f_filing_detail_urls_in_list(text_edgar_current_events, edgar_13f_list)

    for urls_13f in all_urls_13f:
        filing_detail_13f_text = grab_text(urls_13f)
        xml_links = get_primary_doc_and_infotable_urls(filing_detail_13f_text)
        get_primary_doc_xml_urls_in_list(xml_links, primary_doc_list)
        get_infotable_xml_urls_in_list(xml_links, infotable_list)

    # # create for loop and use one row function to get cik
    # for primary_doc in primary_doc_list:
    #     primary_doc_parser(primary_doc)
    # # create for loop and use infotable function to get database
    # df = pd.DataFrame()
    # for infotable in infotable_list:
    #     infotable_parser(infotable, df)

if __name__ == "__main__":
    main()

print("check")
print(edgar_13f_list)
print(primary_doc_list)
print(infotable_list)
