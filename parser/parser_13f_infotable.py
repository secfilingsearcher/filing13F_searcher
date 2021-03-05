import requests
from xml.etree import ElementTree
import re
import pandas as pd
from itertools import cycle

url = 'https://www.sec.gov/Archives/edgar/data/1846943/000108514621001043/infotable.xml'
getter = requests.get(url)
text = getter.text
root = ElementTree.XML(text)

data = []
cols = ["nameOfIssuer", "titleOfClass", "cusip", "value", "sshPrnamt", "sshPrnamtType","investmentDiscretion", "votingAuthority Sole", "votingAuthority Shared", "votingAuthority None"]


for child in root:
    for child in root:
        data_sub_list = []
        for sub_child in child:
            if re.match("\n", sub_child.text):
                for sub_sub_child in sub_child:
                    data_sub_list.append(sub_sub_child.text)
            else:
                data_sub_list.append(sub_child.text)
        data.append(data_sub_list)

df = pd.DataFrame(data)
df.columns = cols

cycle_cik_for_column = cycle(['insert_cik+here'])
first_column = 0
df.insert(loc=first_column, column='CIK', value=[next(cycle_cik_for_column) for df_column in range(len(df))])

print(df)
