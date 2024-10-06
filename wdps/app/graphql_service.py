from requests import post
from .config import Config

def execute_graphql_query(query, variables=None):
    headers = {'Content-Type': 'application/json'}
    data = {'query': query}
    if variables:
        data['variables'] = variables
    response = post(Config.GRAPHQL_URL, json=data, headers=headers)
    response.raise_for_status()  # Levanta una excepción si ocurre un error HTTP
    return response.json()