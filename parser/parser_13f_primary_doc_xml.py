import requests
from xml.etree import ElementTree


def grab_primary_doc_root(primary_doc_xml):
    getter = requests.get(primary_doc_xml)
    text = getter.text
    root = ElementTree.XML(text)
    return root


def grab_primary_doc_cik(root):
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for cik in root.findall('original:headerData/original:filerInfo/original:filer/original:credentials/original:cik',
                            namespaces):
        return cik.text


def grab_primary_doc_company_name(root):
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}
    for company_name in root.findall('original:formData/original:coverPage/original:filingManager/original:name',
                                     namespaces):
        return company_name.text
