"""This file contains functions that parse primary_doc.xml"""
from xml.etree import ElementTree
import requests


def grab_primary_doc_root(primary_doc_xml):
    """Grabs the root of the primary_doc.xml file"""
    getter = requests.get(primary_doc_xml)
    text = getter.text
    primary_doc_root = ElementTree.XML(text)
    return primary_doc_root


def grab_primary_doc_cik(primary_doc_root):
    """Returns the cik from the cik tag on the primary_doc.xml file"""
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for cik in primary_doc_root.findall(
            'original:headerData/original:filerInfo/'
            'original:filer/original:credentials/original:cik',
            namespaces):
        return cik.text


def grab_primary_doc_company_name(primary_doc_root):
    """Returns the company name from the name tag on the primary_doc.xml file"""
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for company_name in primary_doc_root.findall(
            'original:formData/original:coverPage/original:filingManager/original:name',
            namespaces):
        return company_name.text


def grab_primary_doc_accepted_filing_date(primary_doc_root):
    """function docstring"""
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for accepted_filing_date in primary_doc_root.findall(
            'original:formData/original:signatureBlock/original:signatureDate',
            namespaces):
        return accepted_filing_date.text
