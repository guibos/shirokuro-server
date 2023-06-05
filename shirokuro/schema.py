import strawberry

import account.schema


class Query(account.schema.Query):
    pass


class Mutation(account.schema.Mutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
