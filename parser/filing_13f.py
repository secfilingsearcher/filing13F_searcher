"""This file contains functions that parse primary_doc.xml"""
from xml.etree import ElementTree
from crawler_current_events import get_text
from models import EdgarFiling


def get_primary_doc(accession_no_value, cik_value, company_name, filing_date):
    """Gets the data input as parameter from primary_doc.xml and 13f filing webpage
    and instantiates an object"""
    row = EdgarFiling(accession_no=accession_no_value,
                      cik_no=cik_value,
                      company_name=company_name,
                      filing_date=filing_date)
    return row


def get_primary_doc_root(primary_doc_xml):
    """Gets the root of the primary_doc.xml file"""
    text = get_text(primary_doc_xml)
    primary_doc_root = ElementTree.XML(text)
    return primary_doc_root


def get_primary_doc_cik(primary_doc_root):
    """Returns the cik from the cik tag on the primary_doc.xml file"""
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for cik in primary_doc_root.findall(
            'original:headerData/original:filerInfo/'
            'original:filer/original:credentials/original:cik',
            namespaces):
        return cik.text


def get_primary_doc_company_name(primary_doc_root):
    """Returns the company name from the name tag on the primary_doc.xml file"""
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for company_name in primary_doc_root.findall(
            'original:formData/original:coverPage/original:filingManager/original:name',
            namespaces):
        return company_name.text


def get_primary_doc_accepted_filing_date(primary_doc_root):
    """Returns the filing date from the signatureDate tag on the primary_doc.xml file"""
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for accepted_filing_date in primary_doc_root.findall(
            'original:formData/original:signatureBlock/original:signatureDate',
            namespaces):
        return accepted_filing_date.text
