import pandas as pd
from crawler_edgar_current_events import grab_text
from crawler_edgar_current_events import get_13f_filing_detail_urls_in_list
from crawler_edgar_current_events import get_primary_doc_and_infotable_urls
from crawler_edgar_current_events import get_primary_doc_xml_urls_in_list
from crawler_edgar_current_events import get_infotable_xml_urls_in_list
from parser_13f_primary_doc_xml import grab_primary_doc_root
from parser_13f_primary_doc_xml import grab_primary_doc_cik
from parser_13f_primary_doc_xml import grab_primary_doc_company_name
from parser_13f_infotable_xml import infotable_parser

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

    for primary_doc_xml in primary_doc_list:
        root = grab_primary_doc_root(primary_doc_xml)
        cik = grab_primary_doc_cik(root)
        company_name = grab_primary_doc_company_name(root)

    df = pd.DataFrame()
    for infotable_xml in infotable_list:
        pass
    # for infotable in infotable_list:
    #     infotable_parser(infotable, df)

if __name__ == "__main__":
    main()

print("check")
print(edgar_13f_list)
print(primary_doc_list)
print(infotable_list)
