import requests
from xml.etree import ElementTree


def primary_doc_parser(primary_doc_xml):
    url = primary_doc_xml
    getter = requests.get(url)
    text = getter.text
    root = ElementTree.XML(text)

    # grab CIK & company name
    # TODO; dynamically create namespaces
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}

    for cik in root.findall('original:headerData/original:filerInfo/original:filer/original:credentials/original:cik',
                            namespaces):
        pass
        # print(cik.text)
        # return cik.text

    for company_name in root.findall('original:formData/original:coverPage/original:filingManager/original:name',
                                     namespaces):
       pass
       # print(company_name.text)
       # return company_name.text

    # TODO; return cik and company name
