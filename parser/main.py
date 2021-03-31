"""This file returns the cik_value, company name, and infotable data"""
from crawler_current_events import get_text, get_13f_filing_detail_urls, get_sec_accession_no, \
    get_primary_doc_and_infotable_urls, get_primary_doc_xml_url, get_infotable_xml_url
from database_connection import session
from infotable_xml import get_infotable
from primary_doc_xml import get_primary_doc_root, get_primary_doc_cik, \
    get_primary_doc_company_name, get_primary_doc_accepted_filing_date, get_primary_doc


def main():
    """This function returns the cik_value, company name, and infotable data"""
    url_edgar_current_events = 'https://www.sec.gov/cgi-bin/current?q1=1&q2=0&q3=13f'
    text_edgar_current_events = get_text(url_edgar_current_events)
    filing_detail_urls = get_13f_filing_detail_urls(text_edgar_current_events)

    if not filing_detail_urls:
        print("There are no urls on the page")
        return

    for filing_detail_url in filing_detail_urls:
        filing_detail_text = get_text(filing_detail_url)
        accession_no = get_sec_accession_no(filing_detail_text)
        xml_links = get_primary_doc_and_infotable_urls(filing_detail_text)
        primary_doc_xml_url = get_primary_doc_xml_url(xml_links)
        infotable_xml_url = get_infotable_xml_url(xml_links)

        root = get_primary_doc_root(primary_doc_xml_url)
        cik = get_primary_doc_cik(root)
        company_name = get_primary_doc_company_name(root)
        filing_date = get_primary_doc_accepted_filing_date(root)
        primary_doc_row = get_primary_doc(accession_no, cik, company_name, filing_date)
        session.add(primary_doc_row)

        infotable_table = get_infotable(infotable_xml_url, accession_no, cik)
        session.add_all(infotable_table)

        session.commit()


if __name__ == "__main__":
    main()
