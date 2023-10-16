import strawberry
from strawberry_django import auth

from account.types.user_input import UserInput
from account.types.user_type import UserType


@strawberry.type
class Query:
    me: UserType = auth.current_user()


@strawberry.type
class Mutation:
    login: UserType = auth.login()
    logout = auth.logout()
    register: UserType = auth.register(UserInput)
