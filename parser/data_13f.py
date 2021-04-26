"""This file contains functions that parse infotable.xml"""
from xml.etree import ElementTree
from crawler_current_events import get_text
from models import Data13f


def get_infotable(infotable_xml_url, accession_no_value, cik_value):
    """Gets the data from infotable.xml and returns the data as a list of infotable objects"""
    infotable_root = get_infotable_doc_root(infotable_xml_url)
    data = []
    for info in infotable_root.findall('{*}infoTable'):
        infotable_row = Data13f(
            accession_no=accession_no_value,
            cik_no=cik_value,
            nameOfIssuer=get_xml_text(info, '{*}nameOfIssuer'),
            titleOfClass=get_xml_text(info, '{*}titleOfClass'),
            cusip=get_xml_text(info, '{*}cusip'),
            value=get_xml_text(info, '{*}value'),
            sshPrnamt=get_xml_text(info, '{*}shrsOrPrnAmt/{*}sshPrnamt'),
            sshPrnamtType=get_xml_text(info, '{*}sshPrnamtType'),
            putCall=get_xml_text(info, '{*}putCall'),
            investmentDiscretion=get_xml_text(info, '{*}investmentDiscretion'),
            otherManager=get_xml_text(info, '{*}otherManager'),
            votingAuthority_Sole=get_xml_text(info, '{*}votingAuthority/{*}Sole'),
            votingAuthority_Shared=get_xml_text(info, '{*}votingAuthority/{*}Shared'),
            votingAuthority_None=get_xml_text(info, '{*}votingAuthority/{*}None')
        )
        infotable_row.equity_holdings_id = infotable_row.create_filing_13f_primary_key()
        data.append(infotable_row)
    return data


def get_infotable_doc_root(infotable_xml):
    """Gets the root of the infotable.xml file"""
    text = get_text(infotable_xml)
    infotable_root = ElementTree.XML(text)
    return infotable_root


def get_xml_text(dom, xpath):
    """Returns the text from the xml tag on an xml file"""
    node = dom.find(xpath)
    if node is not None:
        return node.text
    return None