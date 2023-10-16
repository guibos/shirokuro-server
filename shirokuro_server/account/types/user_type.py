import strawberry_django
from django.contrib.auth import get_user_model
from strawberry import auto


@strawberry_django.type(get_user_model())
class UserType:
    username: auto
    email: auto
    # region: auto
    # language: auto
