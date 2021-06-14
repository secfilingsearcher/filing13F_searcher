# pylint: disable=too-few-public-methods
"""This file create a class Parser"""
import re
from xml.etree import ElementTree

from edgar_filing_searcher.models import Company, EdgarFiling
from edgar_filing_searcher.parsers.crawler_current_events import get_text
from edgar_filing_searcher.parsers.data_13f import data_13f_row
from edgar_filing_searcher.parsers.errors import CantFindUrlException


class Parser:
    """This class Parser parses 13f filings"""

    def __init__(self, filing_detail_url):
        self.filing_detail_text = get_text(filing_detail_url)
        self.company = None
        self.edgar_filing = None
        self.data_13f = None
        self._parse()

    @staticmethod
    def _parse_sec_accession_no(text_13f):
        """Returns the sec accession number from the 13f filing detail page"""
        return re \
            .search('(?<=Accession <acronym title="Number">No.</acronym></strong> )(.*)',
                    text_13f).group(0)

    @staticmethod
    def _parse_primary_doc_xml_and_infotable_xml_urls(text_13f):
        """Returns the primary_doc.xml and infotable.xml base urls"""
        return re.findall('(?<=<a href=")(.*)(?=">.*.xml)', text_13f, flags=re.IGNORECASE)

    @staticmethod
    def _parse_primary_doc_xml_url(suffix_xml_urls):
        """Adds base url to suffix url for primary_doc.xml url"""
        base_sec_url = "https://www.sec.gov"
        if suffix_xml_urls:
            return base_sec_url + suffix_xml_urls[0]
        raise CantFindUrlException("primary_doc_xml_url suffix is empty")

    @staticmethod
    def _parse_infotable_xml_url(partial_xml_url):
        """Adds base url to suffix url for infotable.xml url"""
        base_sec_url = "https://www.sec.gov"
        if partial_xml_url:
            return base_sec_url + partial_xml_url[-1]
        raise CantFindUrlException("infotable_xml_url suffix is empty")

    @staticmethod
    def _parse_primary_doc_root(primary_doc_xml):
        """Gets the root of the primary_doc.xml file"""
        text = get_text(primary_doc_xml)
        primary_doc_root = ElementTree.XML(text)
        return primary_doc_root

    @staticmethod
    def _parse_primary_doc_cik(primary_doc_root):
        """Returns the cik from the cik tag on the primary_doc.xml file"""
        namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                      'ns1': 'http://www.sec.gov/edgar/common'}
        for cik in primary_doc_root.findall(
                'original:headerData/original:filerInfo/'
                'original:filer/original:credentials/original:cik',
                namespaces):
            return cik.text

    @staticmethod
    def _parse_primary_doc_company_name(primary_doc_root):
        """Returns the company name from the name tag on the primary_doc.xml file"""
        namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                      'ns1': 'http://www.sec.gov/edgar/common'}
        for company_name in primary_doc_root.findall(
                'original:formData/original:coverPage/original:filingManager/original:name',
                namespaces):
            return company_name.text

    @staticmethod
    def _parse_primary_doc_accepted_filing_date(primary_doc_root):
        """Returns the filing date from the signatureDate tag on the primary_doc.xml file"""
        namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                      'ns1': 'http://www.sec.gov/edgar/common'}
        for accepted_filing_date in primary_doc_root.findall(
                'original:formData/original:signatureBlock/original:signatureDate',
                namespaces):
            return accepted_filing_date.text

    def _parse(self):
        accession_no = self._parse_sec_accession_no(self.filing_detail_text)
        xml_links = self._parse_primary_doc_xml_and_infotable_xml_urls(self.filing_detail_text)
        primary_doc_xml_url = self._parse_primary_doc_xml_url(xml_links)
        infotable_xml_url = self._parse_infotable_xml_url(xml_links)

        root = self._parse_primary_doc_root(primary_doc_xml_url)
        cik = self._parse_primary_doc_cik(root)
        company_name = self._parse_primary_doc_company_name(root)
        filing_date = self._parse_primary_doc_accepted_filing_date(root)

        self.company = Company(
            cik_no=cik,
            company_name=company_name,
            filing_count=1
        )

        self.edgar_filing = EdgarFiling(
            accession_no=accession_no,
            cik_no=cik,
            filing_date=filing_date)

        self.data_13f = data_13f_row(infotable_xml_url, accession_no, cik)
