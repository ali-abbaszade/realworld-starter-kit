from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def create_user_object(username, email, password):
        return User.objects.create_user(
            username=username, email=email, password=password
        )

    return create_user_object
