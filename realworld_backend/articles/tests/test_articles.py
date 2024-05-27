from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker
import pytest

from articles import models

User = get_user_model()


@pytest.mark.django_db
def test_list_articles_should_returns_200():
    articles = baker.make(models.Article, _quantity=10)

    client = APIClient()
    response = client.get("/api/articles/")

    assert response.status_code == 200
    assert response.data["count"] == 10


@pytest.mark.django_db
def test_list_articles_filter_by_author_returns_200():
    article = baker.make(models.Article)

    client = APIClient()
    response = client.get(
        f"/api/articles?author={article.author.username}", follow=True
    )

    assert response.status_code == 200
    assert response.data["results"][0]["author"]["username"] == article.author.username
