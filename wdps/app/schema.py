import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, WDPS!")

schema = graphene.Schema(query=Query)