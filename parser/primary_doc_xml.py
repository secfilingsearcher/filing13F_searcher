"""primary doc module docstring"""
from xml.etree import ElementTree
import requests


def grab_primary_doc_root(primary_doc_xml):
    """function docstring"""
    getter = requests.get(primary_doc_xml)
    text = getter.text
    primary_doc_root = ElementTree.XML(text)
    return primary_doc_root


def grab_primary_doc_cik(primary_doc_root):
    """function docstring"""
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for cik in primary_doc_root.findall(
            'original:headerData/original:filerInfo/'
            'original:filer/original:credentials/original:cik',
            namespaces):
        return cik.text


def grab_primary_doc_company_name(primary_doc_root):
    """function docstring"""
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for company_name in primary_doc_root.findall(
            'original:formData/original:coverPage/original:filingManager/original:name',
            namespaces):
        return company_name.text
