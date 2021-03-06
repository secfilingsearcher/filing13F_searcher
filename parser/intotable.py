import requests
from xml.etree import ElementTree
import re
import pandas as pd
from itertools import cycle

def infotable_parser(infotable_xml):
    url = infotable_xml
    getter = requests.get(url)
    text = getter.text
    root = ElementTree.XML(text)
    print(root)

    data = []

infotable_parser('https://www.sec.gov/Archives/edgar/data/1846943/000108514621001043/infotable.xml')