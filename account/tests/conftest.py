import pytest
from django.contrib import auth as django_auth

UserModel = django_auth.get_user_model()


@pytest.fixture
def user() -> UserModel:
    user = UserModel.objects.create_user(username="user", password="password")
    return user
