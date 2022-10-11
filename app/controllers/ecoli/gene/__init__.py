import os
from flask import Response
from flask import make_response
from .web_services import WServices
from .adapters.txt import format_txt_gene
from .adapters.pdf import format_pdf_gene


class Gene_collection:

    format_available = ["jsontable", "jsongql", "pdf", "txt"]
    allCitations = []

    def __init__(self, gql_service, browser_url):
        self.gql_service = gql_service
        self.browser_url = browser_url
        self.response = ""

    def search(self, keyword, page=0,limit=50):
        ws = WServices(self.gql_service)
        results = ws.getSearch({"search": keyword,"page": page,"limit":limit})
        return results

    def getGeneById(self, id, format):
        if format not in self.format_available:
            return 'invalid format: ' + format
        #data = self.check_cache(format, id)
        try:
            ws = WServices(self.gql_service)
            gene = ws.GetGeneById({"advancedSearch": "'"+id+"'[_id]"})
            if format == "jsongql":
                return gene
            elif format == "txt":
                return Response(
                    format_txt_gene(gene),
                    mimetype="text/plain; charset=utf-8",
                    headers={
                        "Content-disposition": "attachment; filename=ecoli_gene_" + id + "_" + ".txt"}
                )
            elif format == "pdf":
                return format_pdf_gene(id,gene,self.gql_service,self.browser_url)
            return gene
        except Exception as e:
            print(e)
            return "ups... error"+str(e)

    def setCitations(self, allCitations):
        self.allCitations = allCitations

    def getAllGene(self, format):
        ws = WServices(self.gql_service)
        genes = ws.getAll_genes()
        if format not in self.format_available:
            self.response = ""
            return ""
        return ""

    def check_cache(self, format, queryType, id):
        data = False
        if os.path.exists("./cache/" + queryType + "_" + format + "_" + id + ".cache"):
            try:
                return open("./cache/" + queryType + "_" + format + "_" + id + ".cache", "r").read()
            except Exception as e:
                print(e)
        return data
