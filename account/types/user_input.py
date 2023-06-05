import strawberry
from django.contrib.auth import get_user_model
from strawberry import auto


@strawberry.django.input(get_user_model())
class UserInput:
    username: auto
    password: auto
