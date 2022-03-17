from .querys import Querys


class WServices:

    querys = Querys()

    def __init__(self, gql_service, advanced_search):
        self.gql_service = gql_service
        self.advanced_search = advanced_search
        self.query = self.querys.getDatasets
        self.variables = {"advancedSearch": advanced_search}

    def get_data(self):
        data = self.gql_service(self.query, self.variables)
        return data['data']['getDatasetsFromSearch']
