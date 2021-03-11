import requests
from xml.etree import ElementTree
import re
import pandas as pd
from itertools import cycle


def grab_infotable_doc_root(infotable_xml):
    url = infotable_xml
    getter = requests.get(url)
    text = getter.text
    infotable_root = ElementTree.XML(text)
    return infotable_root


def initialize_dataframe_with_columns():
    new_cols = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType', 'putCall',
                'investmentDiscretion', 'otherManager', 'votingAuthority_Sole', 'votingAuthority_Shared',
                'votingAuthority_None']
    dataframe = pd.DataFrame()
    dataframe[new_cols] = None
    return dataframe


def fill_dataframe(infotable_root, dataframe):
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

    for info in infotable_root.findall('{*}infoTable'):
        nameOfIssuer = info.find('{*}nameOfIssuer')
        if nameOfIssuer is not None:
            nameOfIssuer_list.append(nameOfIssuer.text)

        titleOfClass = info.find('{*}titleOfClass')
        if titleOfClass is not None:
            titleOfClass_list.append(titleOfClass.text)

        cusip = info.find('{*}cusip')
        if cusip is not None:
            cusip_list.append(cusip.text)

        value = info.find('{*}value')
        if value is not None:
            value_list.append(value.text)

        for shrsOr in info.findall('{*}shrsOrPrnAmt'):
            sshPrnamt = shrsOr.find('{*}sshPrnamt')
            if sshPrnamt is not None:
                sshPrnamt_list.append(sshPrnamt.text)

            sshPrnamtType = shrsOr.find('{*}sshPrnamtType')
            if sshPrnamtType is not None:
                sshPrnamtType_list.append(sshPrnamtType.text)

        #TODO; these have empty spaces when added. need to fire out how to preserve empty space

        # putCall = info.find('{*}putCall')
        # if putCall is not None:
        #     putCall_list.append(putCall.text)

        investmentDiscretion = info.find('{*}investmentDiscretion')
        if investmentDiscretion is not None:
            investmentDiscretion_list.append(investmentDiscretion.text)

        otherManager = info.find('{*}otherManager')
        if otherManager is not None:
            otherManager_list.append(otherManager.text)

        for voting in info.findall('{*}votingAuthority'):
            votingAuthority_Sole = voting.find('{*}Sole')
            if votingAuthority_Sole is not None:
                votingAuthority_Sole_list.append(votingAuthority_Sole.text)

            votingAuthority_Shared = voting.find('{*}Shared')
            if votingAuthority_Shared is not None:
                votingAuthority_Shared_list.append(votingAuthority_Shared.text)

            votingAuthority_None = voting.find('{*}None')
            if votingAuthority_None is not None:
                votingAuthority_None_list.append(votingAuthority_None.text)

    if nameOfIssuer_list:
        dataframe['nameOfIssuer'] = nameOfIssuer_list
    if titleOfClass_list:
        dataframe['titleOfClass'] = titleOfClass_list
    if cusip_list:
        dataframe['cusip'] = cusip_list
    if value_list:
        dataframe['value'] = value_list
    if sshPrnamt_list:
        dataframe['sshPrnamt'] = sshPrnamt_list
    if sshPrnamtType_list:
        dataframe['sshPrnamtType'] = sshPrnamtType_list
    if putCall_list:
        print(putCall_list)
        dataframe['putCall'] = putCall_list
    if investmentDiscretion_list:
        dataframe['investmentDiscretion'] = investmentDiscretion_list
    # if otherManager_list:
    #     dataframe['otherManager'] = otherManager_list
    if votingAuthority_Sole_list:
        dataframe['votingAuthority_Sole'] = votingAuthority_Sole_list
    if votingAuthority_Shared_list:
        dataframe['votingAuthority_Shared'] = votingAuthority_Shared_list
    if votingAuthority_None_list:
        dataframe['votingAuthority_None'] = votingAuthority_None_list
    print('comp')

# root = grab_infotable_doc_root('https://www.sec.gov/Archives/edgar/data/1846943/000108514621001043/infotable.xml')
# df1 = initialize_dataframe_with_columns()
# fill_dataframe(root, df1)
# df1 = df1[0:0]
# print(df1.head(10))
