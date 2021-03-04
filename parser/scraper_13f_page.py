import requests
from xml.etree import ElementTree
import re
import pandas as pd
from itertools import cycle

url = 'https://www.sec.gov/Archives/edgar/data/1532842/000158064221000956/primary_doc.xml'
getter = requests.get(url)
text = getter.text
root = ElementTree.XML(text)

# <credentials>
# <cik>0001532842</cik>
# <ccc>XXXXXXXX</ccc>
# </credentials>
# </filer>
# <periodOfReport>12-31-2020</periodOfReport>
# </filerInfo>
# </headerData>
# <formData>
# <coverPage>
# <reportCalendarOrQuarter>12-31-2020</reportCalendarOrQuarter>
# <isAmendment>false</isAmendment>
# <filingManager>
# <name>BTS Asset Management, Inc.</name>

# grab company name

# grab CIK

print(text)