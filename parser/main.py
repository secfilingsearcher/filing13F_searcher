"""This file returns the cik, company name, and infotable data"""
from crawler_current_events import get_text
from crawler_current_events import get_13f_filing_detail_urls
from crawler_current_events import get_sec_accession_no
from crawler_current_events import get_primary_doc_and_infotable_urls
from crawler_current_events import get_primary_doc_xml_url
from crawler_current_events import get_infotable_xml_url
from infotable_xml import get_infotable
from primary_doc_xml import get_primary_doc_root
from primary_doc_xml import get_primary_doc_cik
from primary_doc_xml import get_primary_doc_company_name
from primary_doc_xml import get_primary_doc_accepted_filing_date
from primary_key_generator import primary_key_generator


def main():
    """This function returns the cik, company name, and infotable data"""
    url_edgar_current_events = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'
    text_edgar_current_events = get_text(url_edgar_current_events)
    filing_detail_urls = get_13f_filing_detail_urls(text_edgar_current_events)

    for filing_detail_url in filing_detail_urls:
        filing_detail_text = get_text(filing_detail_url)
        sec_accession_no = get_sec_accession_no(filing_detail_text)
        xml_links = get_primary_doc_and_infotable_urls(filing_detail_text)
        primary_doc_xml_url = get_primary_doc_xml_url(xml_links)
        infotable_xml_url = get_infotable_xml_url(xml_links)

        root = get_primary_doc_root(primary_doc_xml_url)
        cik = get_primary_doc_cik(root)
        company_name = get_primary_doc_company_name(root)
        filing_date = get_primary_doc_accepted_filing_date(root)
        print(cik, company_name, filing_date)

        df_infotable = get_infotable(infotable_xml_url)
        df_infotable.insert(loc=0, column='accession_no', value=sec_accession_no)
        df_infotable.insert(loc=1, column='cik_id', value=cik)
        df_infotable.insert(loc=2, column='filing_date', value=filing_date)
        print(df_infotable.head())


if __name__ == "__main__":
    main()
