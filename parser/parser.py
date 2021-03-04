import requests
import re
# import unicodedata2

url = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'

getter = requests.get(url)

text = getter.text

company_name = []

print(text)

for filing_name in re.findall('</a>(?!.+</a>)\s*(\w.+)', text, flags=0):
    company_url = re.findall('(?<=<a href=")(.*)(?=">13F-HR</a>)', text, flags=0)
    # https: // www.sec.gov / Archives / edgar / data / 1532842 / 00015
    # 80642 - 21 - 000
    # 956 - index.html
    # filing_url2 = unicodedata2.normalize('NFC', filing_url)
    # print(filing_url2)
    print(filing_name)
    print(company_url)


