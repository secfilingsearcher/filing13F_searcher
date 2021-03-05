import requests
from xml.etree import ElementTree


def primary_doc_parser(primary_doc_xml):
    url = primary_doc_xml
    getter = requests.get(url)
    text = getter.text
    root = ElementTree.XML(text)

    # grab CIK & company name
    namespaces = {'original': 'http://www.sec.gov/edgar/thirteenffiler',
                  'ns1': 'http://www.sec.gov/edgar/common'}

    for cik in root.findall('original:headerData/original:filerInfo/original:filer/original:credentials/original:cik',
                            namespaces):
        print(cik.text)

    for company_name in root.findall('original:formData/original:coverPage/original:filingManager/original:name',
                                     namespaces):
        print(company_name.text)


# primary_doc_parser('https://www.sec.gov/Archives/edgar/data/1532842/000158064221000956/primary_doc.xml')