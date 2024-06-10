from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

import pytest


User = get_user_model()


@pytest.mark.django_db
def test_get_profile_anonymous_returns_401(api_client, create_user):
    user = create_user(username="a", email="test@email.com", password="test")

    response = api_client.get(f"/api/profiles/{user.username}/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_profile_authenticated_returns_200(api_client, create_user):
    user = create_user(username="a", email="test@email.com", password="test")

    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/profiles/{user.username}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "a"
