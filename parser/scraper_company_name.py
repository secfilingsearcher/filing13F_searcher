import requests
import re
# import unicodedata2

url = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'

getter = requests.get(url)

text = getter.text

for filing_name in re.findall('</a>(?!.+</a>)\s*(\w.+)', text, flags=0):
    # filing_url2 = unicodedata2.normalize('NFC', filing_url)
    # print(filing_url2)
    print(filing_name)
