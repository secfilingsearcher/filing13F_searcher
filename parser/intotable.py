import requests
from xml.etree import ElementTree
import re
import pandas as pd
from itertools import cycle


def infotable_parser(infotable_xml, dataframe):
    url = infotable_xml
    getter = requests.get(url)
    text = getter.text
    root = ElementTree.XML(text)

    new_cols = ['nameOfIssuer','titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType', 'putCall', 'investmentDiscretion', 'otherManager', 'votingAuthority Sole', 'votingAuthority Shared', 'votingAuthority None']
    dataframe[new_cols] = None

    nameOfIssuer_list = []
    for infoTable in root.findall('{*}infoTable'):
        nameOfIssuer = infoTable.find('{*}nameOfIssuer')
        nameOfIssuer_list.append(nameOfIssuer.text)
    df['nameOfIssuer'] = nameOfIssuer_list


df = pd.DataFrame()
infotable_parser('https://www.sec.gov/Archives/edgar/data/1846943/000108514621001043/infotable.xml', df)
print(df)
