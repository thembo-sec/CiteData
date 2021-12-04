__version__ = '0.0.1'
__author__ = 'Alyx'

from bs4 import BeautifulSoup

# import xmltodict
# import xml.dom.minidom
# import xml.etree.ElementTree as ET
from xmlCite import Citation

# TODO Figure out affiliation properly, need to parse entire string, delim ';' then add affilliation to each auth
# TODO Get list of all potential metadata
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
    paperlist.append(Citation(paper))

for paper in paperlist:
    paper.authors
    paper.affiliations


