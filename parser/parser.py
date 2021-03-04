import requests
import re
# import unicodedata2

url = 'https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=13F'

getter = requests.get(url)

text = getter.text

company_name = []

# print(re.findall('</a>(?!.+</a>)\s*(\w.+)', text, flags=0))

# company_list = re.search('</strong><hr>.*<hr></pre>', text, re.DOTALL)
# grouped = company_list.group(0)
# print(str(grouped))
#

for company_info in re.findall('(?<=03-03-2021)(.*)', text, flags=0):
    filing_name = re.search('</a>(?!.+</a>)\s*(\w.+)', company_info)
    company_url = re.search('(?<=<a href=")(.*)(?=">13F-HR</a>)', company_info)
    print(company_url)
    print(filing_name)


