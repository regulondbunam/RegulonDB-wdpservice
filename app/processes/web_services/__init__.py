query = '''query REGULONDB_INFO{
    getDatabaseInfo{
        regulonDBVersion
    }
}
'''

def get_RegulonDB_version(gql_service):
    data = gql_service(query)
    return data["data"]["getDatabaseInfo"][0]