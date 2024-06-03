from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
import pytest

from articles import models
from users.models import Follow

User = get_user_model()


@pytest.mark.django_db
def test_list_articles_should_returns_200(api_client):
    articles = baker.make(models.Article, _quantity=10)

    response = api_client.get("/api/articles/")

    assert response.status_code == 200
    assert response.data["count"] == 10


@pytest.mark.django_db
def test_list_articles_filter_by_author_returns_200(api_client):
    article = baker.make(models.Article)

    response = api_client.get(
        f"/api/articles?author={article.author.username}", follow=True
    )

    assert response.status_code == 200
    assert response.data["results"][0]["author"]["username"] == article.author.username


@pytest.mark.django_db
def test_list_articles_filter_by_favorited_returns_200(api_client):
    user = baker.make(User)
    article = baker.make(models.Article)
    favorite = baker.make(models.Favorite, user=user, article=article)

    response = api_client.get(f"/api/articles?favorited={user.username}", follow=True)

    assert response.status_code == 200
    assert response.data["results"][0]["favorites_count"] == 1


def test_list_feed_articles_anonymous_returns_401(api_client):

    response = api_client.get("/api/articles/feed/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_feed_articles_authenticated_user_returns_200(api_client):
    user1 = baker.make(User)
    user2 = baker.make(User)
    Follow.objects.create(follower=user1, following=user2)
    baker.make(models.Article, author=user2)

    api_client.force_authenticate(user=user1)

    response = api_client.get("/api/articles/feed/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["author"]["following"] == True
    assert response.data[0]["author"]["username"] == user2.username


@pytest.mark.django_db
def test_get_single_article_returns_200(api_client):
    article = baker.make(models.Article)

    response = api_client.get(f"/api/articles/{article.slug}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["slug"] == article.slug
    assert response.data["title"] == article.title


@pytest.mark.django_db
def test_create_article_anonymous_user_returns_401(api_client):
    user = User.objects.create()

    response = api_client.post(
        "/api/articles/",
        {"title": "a", "slug": "a", "body": "a", "tags": ["a"], "author": user},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_article_authenticated_user_invalid_data_returns_400(api_client):
    user = User.objects.create()

    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/api/articles/",
        {"title": "", "slug": "", "body": "", "tags": [], "author": user},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_article_authenticated_user_valid_data_returns_201(api_client):
    user = User.objects.create()

    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/api/articles/",
        {"title": "a", "slug": "a", "body": "a", "tags": ["a"], "author": user},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "a"


@pytest.mark.django_db
def test_update_article_anonymous_user_returns_401(api_client):
    article = baker.make(models.Article)

    response = api_client.put(f"/api/articles/{article.slug}/")

    response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_article_authenticate_user_invalid_data_returns_400(api_client):
    user = baker.make(User)
    article = baker.make(models.Article)

    api_client.force_authenticate(user=user)
    response = api_client.put(f"/api/articles/{article.slug}/", {"title": ""})

    response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_article_authenticate_user_valid_data_returns_200(api_client):
    user = baker.make(User)
    article = baker.make(models.Article)

    api_client.force_authenticate(user=user)
    response = api_client.put(
        f"/api/articles/{article.slug}/", {"title": "a", "body": "abc", "tags": ["a"]}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "a"
    assert response.data["body"] == "abc"


@pytest.mark.django_db
def test_delete_article_anonymous_user_returns_401(api_client):
    article = baker.make(models.Article)

    response = api_client.delete(f"/api/articles/{article.slug}/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_article_authenticated_user_returns_204(api_client):
    article = baker.make(models.Article)

    api_client.force_authenticate(user=User())
    response = api_client.delete(f"/api/articles/{article.slug}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_favorite_article_anonymous_returns_401(api_client):
    article = baker.make(models.Article)

    response = api_client.post(f"/api/articles/{article.slug}/favorite/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_favorite_article_authenticated_user_returns_200(api_client):
    article = baker.make(models.Article)
    user = baker.make(User)

    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/articles/{article.slug}/favorite/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["favorited"] == True
    assert response.data["slug"] == article.slug
    assert response.data["title"] == article.title


@pytest.mark.django_db
def test_unfavorite_article_anonymous_returns_401(api_client):
    article = baker.make(models.Article)

    response = api_client.delete(f"/api/articles/{article.slug}/favorite/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_unfavorite_article_authenticated_user_returns_200(api_client):
    article = baker.make(models.Article)
    user = baker.make(User)

    api_client.force_authenticate(user=user)
    response = api_client.delete(f"/api/articles/{article.slug}/favorite/")

    assert response.status_code == status.HTTP_200_OK
