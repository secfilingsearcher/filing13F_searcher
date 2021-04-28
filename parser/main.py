# pylint: disable=import-error
"""This file contains the main method"""
from crawler_current_events import get_text, parse_13f_filing_detail_urls, parse_sec_accession_no, \
    parse_primary_doc_xml_and_infotable_xml_urls, parse_primary_doc_xml_url, parse_infotable_xml_url
from database_connection import session
from data_13f import data_13f_row
from parsing_13f_filing import parse_primary_doc_root, parse_primary_doc_cik, \
    parse_primary_doc_company_name, parse_primary_doc_accepted_filing_date
from models import EdgarFiling, Company

URL_EDGAR_CURRENT_EVENTS = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=13f'


def main():
    """This function returns the cik, company name, and infotable data"""
    text_edgar_current_events = get_text(URL_EDGAR_CURRENT_EVENTS)
    filing_detail_urls = parse_13f_filing_detail_urls(text_edgar_current_events)

    if not filing_detail_urls:
        print("There are no urls on the page")
        return

    for filing_detail_url in filing_detail_urls:
        filing_detail_text = get_text(filing_detail_url)
        accession_no = parse_sec_accession_no(filing_detail_text)
        xml_links = parse_primary_doc_xml_and_infotable_xml_urls(filing_detail_text)
        primary_doc_xml_url = parse_primary_doc_xml_url(xml_links)
        infotable_xml_url = parse_infotable_xml_url(xml_links)

        root = parse_primary_doc_root(primary_doc_xml_url)
        cik = parse_primary_doc_cik(root)
        company_name = parse_primary_doc_company_name(root)
        filing_date = parse_primary_doc_accepted_filing_date(root)
        company_row = Company(
            cik_no=cik,
            company_name=company_name)
        edgar_filing_row = EdgarFiling(
            accession_no=accession_no,
            cik_no=cik,
            filing_date=filing_date)
        session.add(company_row)
        session.add(edgar_filing_row)

        data_13f_table = data_13f_row(infotable_xml_url, accession_no, cik)
        session.add_all(data_13f_table)

        session.commit()


if __name__ == "__main__":
    main()
