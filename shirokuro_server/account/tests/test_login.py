import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_login(user: get_user_model()):
    assert True
