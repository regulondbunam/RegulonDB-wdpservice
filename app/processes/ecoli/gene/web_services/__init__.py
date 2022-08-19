from .Queries import Queries


#data = self.gql_service(self.query, self.variables)

class WServices:
    queries = Queries()

    def __init__(self, gql_service):
        self.gql_service = gql_service

    def getSearch(self,variables):
        try:
            data = self.gql_service(self.queries.GET_GENE_BY_SEARCH, variables)
            return data["data"]["getGenesBy"]
        except Exception as e:
            print("error:",e)
            return {"error": "try"}