"""This file contains functions that parse infotable.xml"""
from xml.etree import ElementTree
import requests
import pandas as pd


def grab_infotable(infotable_xml_url):
    """Extracts the data from infotable.xml"""
    infotable_root = grab_infotable_doc_root(infotable_xml_url)
    columns = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType',
               'putCall', 'investmentDiscretion', 'otherManager', 'votingAuthority_Sole',
               'votingAuthority_Shared', 'votingAuthority_None']
    data = []
    for info in infotable_root.findall('{*}infoTable'):
        # pylint: disable=R0914
        row = [
            get_xml_text(info, '{*}nameOfIssuer'),
            get_xml_text(info, '{*}titleOfClass'),
            get_xml_text(info, '{*}cusip'),
            get_xml_text(info, '{*}value'),
            get_xml_text(info, '{*}shrsOrPrnAmt/{*}sshPrnamt'),
            get_xml_text(info, '{*}sshPrnamtType'),
            get_xml_text(info, '{*}putCall'),
            get_xml_text(info, '{*}investmentDiscretion'),
            get_xml_text(info, '{*}otherManager'),
            get_xml_text(info, '{*}votingAuthority/{*}Sole'),
            get_xml_text(info, '{*}votingAuthority/{*}Shared'),
            get_xml_text(info, '{*}votingAuthority/{*}None')
        ]

        data.append(row)
    return pd.DataFrame(data, columns=columns)


def grab_infotable_doc_root(infotable_xml):
    """Grabs the root of the infotable.xml file"""
    url = infotable_xml
    getter = requests.get(url)
    text = getter.text
    infotable_root = ElementTree.XML(text)
    return infotable_root


def get_xml_text(dom, xpath):
    """Returns the text from the xml tag on an xml file"""
    node = dom.find(xpath)
    if node is not None:
        return node.text
    return None

