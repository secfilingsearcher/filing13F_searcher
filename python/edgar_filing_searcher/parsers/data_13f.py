"""This file contains functions that parse infotable.xml"""
from xml.etree import ElementTree
from edgar_filing_searcher.parsers.crawler_current_events import get_text
from edgar_filing_searcher.models import Data13f


def data_13f_row(infotable_xml_url, accession_no_value, cik_value):
    """Gets the data from infotable.xml and returns the data as a list of infotable objects"""
    infotable_root = parse_infotable_doc_root(infotable_xml_url)
    data = []
    for info in infotable_root.findall('{*}infoTable'):
        infotable_row = Data13f(
            accession_no=accession_no_value,
            cik_no=cik_value,
            name_of_issuer=parse_xml_text(info, '{*}nameOfIssuer'),
            title_of_class=parse_xml_text(info, '{*}titleOfClass'),
            cusip=parse_xml_text(info, '{*}cusip'),
            value=parse_xml_text(info, '{*}value'),
            ssh_prnamt=parse_xml_text(info, '{*}shrsOrPrnAmt/{*}sshPrnamt'),
            ssh_prnamt_type=parse_xml_text(info, '{*}sshPrnamtType'),
            put_call=parse_xml_text(info, '{*}putCall'),
            investment_discretion=parse_xml_text(info, '{*}investmentDiscretion'),
            other_manager=parse_xml_text(info, '{*}otherManager'),
            voting_authority_sole=parse_xml_text(info, '{*}votingAuthority/{*}Sole'),
            voting_authority_shared=parse_xml_text(info, '{*}votingAuthority/{*}Shared'),
            voting_authority_none=parse_xml_text(info, '{*}votingAuthority/{*}None')
        )
        infotable_row.equity_holdings_id = infotable_row.create_data_13f_primary_key()
        data.append(infotable_row)
    return data


def parse_infotable_doc_root(infotable_xml):
    """Gets the root of the infotable.xml file"""
    text = get_text(infotable_xml)
    infotable_root = ElementTree.XML(text)
    return infotable_root


def parse_xml_text(dom, xpath):
    """Returns the text from the xml tag on an xml file"""
    node = dom.find(xpath)
    if node is not None:
        return node.text
    return None
