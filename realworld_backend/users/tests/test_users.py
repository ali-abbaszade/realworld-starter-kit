from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

import pytest
from users import models

User = get_user_model()


@pytest.mark.django_db
def test_register_user_with_valid_data_returns_201(api_client):

    response = api_client.post(
        "/api/users/",
        {
            "username": "abc",
            "email": "test@domain.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "abc"
    assert response.data["email"] == "test@domain.com"


@pytest.mark.django_db
def test_register_user_with_invalid_data_returns_400(api_client):

    response = api_client.post(
        "/api/users/",
        {
            "username": "",
            "email": "test@domain.com",
            "password": "123",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_user_valid_input_returns_200(api_client, create_user):
    user = create_user(username="abc", email="test@email.com", password="testpassword")

    response = api_client.post(
        "/api/users/login/",
        {"email": "test@email.com", "password": "testpassword"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


@pytest.mark.django_db
def test_login_user_invalid_input_returns_400(api_client, create_user):

    user = create_user(username="abc", email="test@email.com", password="testpassword")

    response = api_client.post(
        "/api/users/login/",
        {"email": "wrong@email.com", "password": "wrong"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_current_authenticated_user_returns_200(api_client, create_user):
    user = create_user(username="abc", email="test@email.com", password="testpassword")

    api_client.force_authenticate(user=user)
    response = api_client.get("/api/user/")

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_get_current_anonymous_user_returns_401(api_client, create_user):
    user = create_user(username="a", email="test@email.com", password="test")

    response = api_client.get("/api/user/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_user_anonymous_returns_401(api_client, create_user):
    user = create_user(username="a", email="test@email.com", password="testpassword")

    response = api_client.put(
        "/api/user/", {"email": "updated@test.com", "username": "b"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_user_authenticated_invalid_data_returns_400(api_client, create_user):
    user = create_user(username="a", email="test@email.com", password="testpassword")

    api_client.force_authenticate(user=user)
    response = api_client.put("/api/user/", {"username": "b"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field is required." in str(response.content)


@pytest.mark.django_db
def test_update_user_authenticated_valid_data_returns_200(api_client, create_user):
    user = create_user(username="a", email="test@email.com", password="testpassword")

    api_client.force_authenticate(user=user)
    response = api_client.put(
        "/api/user/", {"email": "update@test.com", "username": "b"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == "update@test.com"
    assert response.data["username"] == "b"


@pytest.mark.django_db
def test_follow_user_anonymous_returns_401(api_client, create_user):
    user1 = create_user(username="a", email="user1@email.com", password="testpassword")
    user2 = create_user(username="b", email="user2@email.com", password="testpassword")

    response = api_client.post(f"/api/profiles/{user2.username}/follow/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_follow_user_authenticated_returns_200(api_client, create_user):
    user1 = create_user(username="a", email="user1@email.com", password="testpassword")
    user2 = create_user(username="b", email="user2@email.com", password="testpassword")

    api_client.force_authenticate(user=user1)
    response = api_client.post(f"/api/profiles/{user2.username}/follow/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user2.username
    assert response.data["following"] == True


@pytest.mark.django_db
def test_unfollow_user_anonymous_returns_401(api_client, create_user):
    user1 = create_user(username="a", email="user1@email.com", password="testpassword")
    user2 = create_user(username="b", email="user2@email.com", password="testpassword")

    follow = models.Follow.objects.create(follower_id=user1.id, following_id=user2.id)

    response = api_client.delete(f"/api/profiles/{user2.username}/follow/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_unfollow_user_authenticated_returns_200(api_client, create_user):
    user1 = create_user(username="a", email="user1@email.com", password="testpassword")
    user2 = create_user(username="b", email="user2@email.com", password="testpassword")

    follow = models.Follow.objects.create(follower_id=user1.id, following_id=user2.id)

    api_client.force_authenticate(user=user1)
    response = api_client.delete(f"/api/profiles/{user2.username}/follow/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user2.username
    assert response.data["following"] == False
