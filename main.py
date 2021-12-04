__version__ = '0.0.1'
__author__ = 'Alyx'

import pandas as pd
from bs4 import BeautifulSoup

# import xmltodict
# import xml.dom.minidom
# import xml.etree.ElementTree as ET
from xmlCite import Citation


def get_particulars(source, i):
    return i, source.title, source.year, source.journal


# TODO doi, isbn

# doc = xml.dom.minidom.parse("CDSS-xml-rawdump.xml")

# with open("CDSS-xml-rawdump.xml", encoding='utf8') as file:
#    doc = xmltodict.parse(file.read())

with open("CDSS-xml-rawdump.xml", encoding='utf8') as file:
    soup = BeautifulSoup(file, 'xml')

papers = soup.find_all('record')

paperlist = []
metalist = []

for paper in papers:

    keys = paper.contents
    for key in keys:
        if key.name:
            if key not in metalist:
                metalist.append(key)

    paperlist.append(Citation(paper))

particulars = []
meta = []
auths = []
keywords = []

for i, paper in enumerate(paperlist):
    particulars.append(get_particulars(paper, i))
    get_meta = [i, paper.metadata]
    get_auth = [i, paper.authors, paper.affiliations]
    get_keywords = [i, paper.keywords]

    meta.append(get_meta)
    auths.append(get_auth)
    keywords.append(get_keywords)

dfp = pd.DataFrame(particulars, columns=('Key', 'Title', 'Year', 'Journal'))
dfm = pd.DataFrame(meta, columns=('Key', 'Metadata'))
dfa = pd.DataFrame(auths, columns=('Key', 'Authors', 'Affiliations'))
dfk = pd.DataFrame(keywords, columns=('Key', 'Keywords'))

with pd.ExcelWriter('Output.xlsx') as writer:
    dfp.to_excel(writer, sheet_name='Particulars')
    dfm.to_excel(writer, sheet_name='Metadata')
    dfa.to_excel(writer, sheet_name='Authors')
    dfk.to_excel(writer, sheet_name='Keywords')
