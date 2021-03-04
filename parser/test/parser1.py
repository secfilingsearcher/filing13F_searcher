import requests
import re
# import unicodedata2

url = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'

getter = requests.get(url)

text = getter.text

for filing_name in re.findall('</a>(?!.+</a>)\s*(\w.+)', text, flags=0):
    print(filing_name)

for filing_name in re.findall('(?<=<a href=")(.*)(?=">13F-HR</a>)', text, flags=0):
    print(filing_name)