from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker

from articles import models
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_add_comment_anonymous_user_returns_401():
    article = baker.make(models.Article)

    client = APIClient()
    response = client.post(f"/api/articles/{article.slug}/comments/")

    response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_add_comment_authenticated_invalid_data_returns_400():
    article = baker.make(models.Article)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        f"/api/articles/{article.slug}/comments/",
        {"body": ""},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_add_comment_authenticated_valid_data_returns_201():
    article = baker.make(models.Article)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        f"/api/articles/{article.slug}/comments/",
        {"body": "abc"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["body"] == "abc"


@pytest.mark.django_db
def test_get_comments_returns_200():
    article = baker.make(models.Article)
    baker.make(models.Comment, _quantity=5, article=article)

    client = APIClient()
    response = client.get(f"/api/articles/{article.slug}/comments/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_delete_comment_anonymous_returns_401():
    comment = baker.make(models.Comment)

    client = APIClient()
    response = client.delete(
        f"/api/articles/{comment.article.slug}/comments/{comment.id}/"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_comment_authenticated_user_returns_204():
    comment = baker.make(models.Comment)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete(
        f"/api/articles/{comment.article.slug}/comments/{comment.id}/"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
