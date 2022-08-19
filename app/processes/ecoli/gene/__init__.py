from imp import init_builtin
from .web_services import WServices

class Gene_collection:
    
    def __init__(self, gql_service):
        self.gql_service = gql_service
    
    def search(self,keyword):
        ws = WServices(self.gql_service)
        results = ws.getSearch({"search": keyword})
        return results