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
            if key.name not in metalist:
                metalist.append(key.name)

    paperlist.append(Citation(paper))

particulars = []
meta = []
auths = []
affiliations =[]
keywords = []

# TODO fix so that there is a row for each entry. Multiple rows per key in some cases
# TODO maybe write class for a list of citations? Could include methods for exporting data
for i, paper in enumerate(paperlist):

    particulars.append(get_particulars(paper, i))
    get_meta = []
    get_auth = []
    get_affil = []
    get_keywords = []

    for key in paper.keywords:
        get_keywords.append([i, key])

    if paper.authors:
        for auth in paper.authors:
            get_auth.append([i, auth])
    else:
        get_auth.append([i, paper.authors])

    if paper.affiliations:
        for affil in paper.affiliations:
            get_affil.append([i, affil])
    else:
        get_affil.append([i, paper.affiliations])

    for metadata in paper.metadata:
        get_meta.append([i, metadata])

    meta.extend(get_meta)
    auths.extend(get_auth)
    affiliations.extend(get_affil)
    keywords.extend(get_keywords)

dfp = pd.DataFrame(particulars, columns=('Key', 'Title', 'Year', 'Journal'))
dfm = pd.DataFrame(meta, columns=('Key', 'Metadata'))
dfa = pd.DataFrame(auths, columns=('Key', 'Authors'))
dfl = pd.DataFrame(affiliations, columns=('Key', 'Affiliations'))
dfk = pd.DataFrame(keywords, columns=('Key', 'Keywords'))

with pd.ExcelWriter('Output.xlsx') as writer:
    dfp.to_excel(writer, sheet_name='Particulars')
    dfm.to_excel(writer, sheet_name='Metadata')
    dfa.to_excel(writer, sheet_name='Authors')
    dfk.to_excel(writer, sheet_name='Keywords')
