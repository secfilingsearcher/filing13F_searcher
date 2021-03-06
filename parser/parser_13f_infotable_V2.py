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

    new_cols = ['nameOfIssuer','titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType', 'putCall', 'investmentDiscretion', 'otherManager', 'votingAuthority_Sole', 'votingAuthority_Shared', 'votingAuthority_None']
    dataframe[new_cols] = None

    nameOfIssuer_list = []
    titleOfClass_list = []
    cusip_list = []
    value_list = []
    sshPrnamt_list = []
    sshPrnamtType_list = []
    putCall_list = []
    investmentDiscretion_list = []
    otherManager_list = []
    votingAuthority_Sole_list = []
    votingAuthority_Shared_list = []
    votingAuthority_None_list = []

    for infoTable in root.findall('{*}infoTable'):
        nameOfIssuer = infoTable.find('{*}nameOfIssuer')
        if nameOfIssuer is not None:
            nameOfIssuer_list.append(nameOfIssuer.text)

        titleOfClass = infoTable.find('{*}titleOfClass')
        titleOfClass_list.append(titleOfClass.text)

        cusip = infoTable.find('{*}cusip')
        cusip_list.append(cusip.text)

        value = infoTable.find('{*}value')
        value_list.append(value.text)

        for shrsOrPrnAmt in infoTable.findall('{*}shrsOrPrnAmt'):
            sshPrnamt = shrsOrPrnAmt.find('{*}sshPrnamt')
            sshPrnamt_list.append(sshPrnamt.text)

            sshPrnamtType = shrsOrPrnAmt.find('{*}sshPrnamtType')
            sshPrnamtType_list.append(sshPrnamtType.text)

        putCall = infoTable.find('{*}putCall')
        if putCall is not None:
            nameOfIssuer_list.append(nameOfIssuer.text)

        investmentDiscretion = infoTable.find('{*}investmentDiscretion')
        investmentDiscretion_list.append(investmentDiscretion.text)

        otherManager = infoTable.find('{*}otherManager')
        if otherManager is not None:
            otherManager_list.append(otherManager.text)

        for votingAuthority in infoTable.findall('{*}votingAuthority'):
            Sole = votingAuthority.find('{*}Sole')
            votingAuthority_Sole_list.append(Sole.text)

            Shared = votingAuthority.find('{*}Shared')
            votingAuthority_Shared_list.append(Shared.text)

            None_ = votingAuthority.find('{*}None')
            votingAuthority_None_list.append(None_.text)


    df['nameOfIssuer'] = nameOfIssuer_list
    df['titleOfClass'] = titleOfClass_list
    df['cusip'] = cusip_list
    df['value'] = value_list
    df['sshPrnamt'] = sshPrnamt_list
    df['sshPrnamtType'] = sshPrnamtType_list
    if putCall_list:
        df['putCall'] = putCall_list
    df['investmentDiscretion'] = investmentDiscretion_list
    if otherManager:
        df['otherManager'] = otherManager_list
    df['votingAuthority_Sole'] = votingAuthority_Sole_list
    df['votingAuthority_Shared'] = votingAuthority_Shared_list
    df['votingAuthority_None'] = votingAuthority_None_list


df = pd.DataFrame()
infotable_parser('https://www.sec.gov/Archives/edgar/data/1846943/000108514621001043/infotable.xml', df)

pd.set_option('display.max_columns', None)
print(df.head(2))
