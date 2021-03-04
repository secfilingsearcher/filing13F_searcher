import requests
from xml.etree import ElementTree
import re
import pandas as pd
from itertools import cycle

url = 'https://www.sec.gov/Archives/edgar/data/1532842/0001580642-21-000956-index.html'
getter = requests.get(url)
text = getter.text

print(text)