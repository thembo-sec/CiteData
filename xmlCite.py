from dataclasses import dataclass


# TODO parse info to fill person class
@dataclass
class Person:
    name: str
    affiliation: str


class Citation(object):
    def __init__(self, document):
        self.soup = document
        self._title = ''

    @property
    def title(self):
        """
        Gets title. Returns 'None' if no title found in xml
        """
        if not self._title:
            if self.soup.find('title'):
                self._title = self.soup.find('title').text.strip()
            else:
                self._title = 'None'

        return self._title

    @property
    def metadata(self):
        """
        Acquires all the metadata tags for this citation entry.
        """
        metadata = []
        tags = self.soup.contents
        for tag in tags:
            if tag.name:
                metadata.append(tag.name)
        return metadata

    @property
    def keywords(self):
        """
        Acquires all the search keywords for the citation entry
        """
        keys = self.soup.find_all('keyword')
        keywords = []
        for key in keys:
            if key.name:
                keywords.append(key.text.strip())

        return keywords

    @property
    def authors(self):
        """
        Gets the list of authors for the entry. Returns False if the citation does not contain that information
        """
        authors = []
        if self.soup.find('author'):
            auth_list = self.soup.find_all('author')

            for auth in auth_list:
                authors.append(auth.text.strip())

            return authors
        else:
            return False

    @property
    def affiliations(self):
        """
        Get the list of affiliations in the paper. Note that some XML files may have a carriage return which is not split.
        """
        affiliations = []
        if self.soup.find('auth-address'):
            addresses = self.soup.find('auth-address').text
            addresses = addresses.split(';')
            for address in addresses:
                affiliations.append(address.strip())

            return affiliations
        else:
            return False

    @property
    def year(self):
        """
        Gets the publication year. Returns False if no year found.
        """
        if self.soup.find('year'):
            year = self.soup.find('year').text.strip()
            return year
        else:
            return False

    @property
    def journal(self):
        """
        Gets the publication journal. Returns False if none found.
        Will search in both periodical and alt-periodical if periodical is not found in the xml
        """
        if self.soup.find('periodical'):
            journal = self.soup.periodical.find('full-title').text.strip()
        elif self.soup.find('alt-periodical'):
            alt = self.soup.find('alt-periodical')
            journal = alt.find('full-title').text.strip()
        else:
            return False
        return journal
