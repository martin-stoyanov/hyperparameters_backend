import graphene
from models.schema import ModelQuery, ModelMutation

class Query(ModelQuery, graphene.ObjectType):
  pass

class Mutation(ModelMutation, graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)
