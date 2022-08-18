from .querys import Querys


#data = self.gql_service(self.query, self.variables)

class WServices:
    querys = Querys()

    def __init__(self, gql_service, variables):
        self.gql_service = gql_service
        self.variables = variables

    def getSearch():
        print("Hola")