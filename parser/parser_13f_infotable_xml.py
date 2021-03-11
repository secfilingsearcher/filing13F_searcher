import requests
from xml.etree import ElementTree
import pandas as pd


def grab_infotable(infotable_xml_url):
    infotable_root = grab_infotable_doc_root(infotable_xml_url)
    columns = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType', 'putCall',
               'investmentDiscretion', 'otherManager', 'votingAuthority_Sole', 'votingAuthority_Shared',
               'votingAuthority_None']
    data = []
    for info in infotable_root.findall('{*}infoTable'):
        nameOfIssuer = get_xml_text(info, '{*}nameOfIssuer')
        titleOfClass = get_xml_text(info, '{*}titleOfClass')
        cusip = get_xml_text(info, '{*}cusip')
        value = get_xml_text(info, '{*}value')
        sshPrnamt = get_xml_text(info, '{*}shrsOrPrnAmt/{*}sshPrnamt')
        sshPrnamtType = get_xml_text(info, '{*}sshPrnamtType')
        putCall = get_xml_text(info, '{*}putCall')
        investmentDiscretion = get_xml_text(info, '{*}investmentDiscretion')
        otherManager = get_xml_text(info, '{*}otherManager')
        votingAuthority_Sole = get_xml_text(info, '{*}votingAuthority/{*}Sole')
        votingAuthority_Shared = get_xml_text(info, '{*}votingAuthority/{*}Shared')
        votingAuthority_None = get_xml_text(info, '{*}votingAuthority/{*}None')

        data.append([nameOfIssuer, titleOfClass, cusip, value, sshPrnamt, sshPrnamtType, putCall, investmentDiscretion,
                     otherManager, votingAuthority_Sole, votingAuthority_Shared, votingAuthority_None])
    return pd.DataFrame(data, columns=columns)


def get_xml_text(dom, xpath):
    node = dom.find(xpath)
    if node is not None:
        return node.text


def grab_infotable_doc_root(infotable_xml):
    url = infotable_xml
    getter = requests.get(url)
    text = getter.text
    infotable_root = ElementTree.XML(text)
    return infotable_root
