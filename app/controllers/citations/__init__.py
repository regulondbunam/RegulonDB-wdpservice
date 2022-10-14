import re


class Citations:

    allCitations = []

    def __init__(self, allCitations):
        self.allCitations = allCitations

    def getIndex_citation_by_id(self, id):
        index = 0
        for citation in self.allCitations:
            if citation["publication"] != None:
                if citation["publication"]["id"] == id:
                    return index
            if citation["evidence"] != None:
                if citation["evidence"]["id"] == id:
                    return index
            index += 1
        return -1

    def citation_toLink(self, index, citation, isSmall=True):
        cit = self.citation_toString(citation, isSmall)
        url = citation["publication"]["url"]
        return f""" <a href="{url}">[{index}] {cit}</a>"""

    def citation_toString(self, citation, isSmall=True):
        publication = ""
        year = ""
        authors = ""
        #pmid = ""
        #url = ""
        #title = ""
        evidence_type = ""
        evidence_code = ""
        #evidence_name = ""
        if citation["publication"] != None:
            if citation['publication']['citation'] != None:
                publication = citation['publication']['citation']
            if citation['publication']['year'] != None:
                year = citation['publication']['year']
            if citation['publication']['authors'] != None:
                authors = citation['publication']['authors']
            # if citation['publication']['pmid'] != None:
            #    pmid = citation['publication']['pmid']
            # if citation['publication']['url'] != None:
            #    url = citation['publication']['url']
            # if citation['publication']['title'] != None:
            #    title = citation['publication']['title']
        if citation["evidence"] != None:
            if citation['evidence']['type'] != None:
                evidence_type = citation['evidence']['type']
            # if citation['evidence']['name'] != None:
            #    evidence_name = citation['evidence']['name']
            if citation['evidence']['code'] != None:
                evidence_code = "["+citation['evidence']['code']+"]"
            if evidence_type == "W":
                evidence_code = f"<b>{evidence_code}</b>"
        if isSmall:
            return f"{authors[0]} et al.{year} {evidence_code}"
        else:
            return f"{publication}.{evidence_code}"

    def getCitation_by_id(self, id):
        index = self.getIndex_citation_by_id(id)
        return {
            "index": index,
            "citation": self.allCitations[index]
        }

    def note(self, note):
        if note == None:
            return ""
        while re.search("(\|CITS:)|\|\.", note):
            note = re.sub("(\|CITS:)|\|\.", "", note)
        safe = 200
        while re.search("\[\s*RDBECOLI(PRC|EVC)[0-9]{5}\]", note) or safe > 200:
            id = re.search("\s*RDBECOLI(PRC|EVC)[0-9]{5}", note).group()
            index_citation = self.getIndex_citation_by_id(id)
            if index_citation != -1:
                citation = self.citation_toLink(
                    index_citation+1, self.allCitations[index_citation], True)
                note = re.sub(
                    "\[\s*RDBECOLI(PRC|EVC)[0-9]{5}\]", citation, note, 1)
            else:
                note = re.sub(
                    "\[\s*RDBECOLI(PRC|EVC)[0-9]{5}\]", " ", note, 1)
        return note

    def list_citations(self):
        citations = []
        index = 1
        for citation in self.allCitations:
            citations.append({
                "index": index,
                "citation": self.citation_toString(citation, False),
                "url": citation["publication"]["url"]
            })
            index += 1
        return citations
