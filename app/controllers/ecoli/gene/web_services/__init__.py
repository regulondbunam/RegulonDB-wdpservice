import os, sys
from app.utiles import errorRegister
from .Queries import Queries


#data = self.gql_service(self.query, self.variables)

class WServices:
    queries = Queries()

    def __init__(self, gql_service):
        self.gql_service = gql_service
    
    def GetGeneById(self,variables):
        try:
            data = self.gql_service(self.queries.GET_GENE_BY_ID, variables)
            return data["data"]["getGenesBy"]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error = f"""on {str(fname)} def format_txt_gene, build txt [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
            errorRegister(error)
            print("error:",e)
            return {"error": "try"}
    
    def getAll_genes(self):
        try:
            data = self.gql_service(self.queries.GET_ALL_GENES)
            return data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error = f"""on {str(fname)} def format_txt_gene, build txt [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
            errorRegister(error)
            print("error:",e)
            return {"error": "try"}

    def getSearch(self,variables):
        try:
            data = self.gql_service(self.queries.GET_GENE_BY_SEARCH, variables)
            return data["data"]["getGenesBy"]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error = f"""on {str(fname)} def format_txt_gene, build txt [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
            errorRegister(error)
            print("error:",e)
            return {"error": "try"}