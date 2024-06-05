from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_article(api_client):
    def send_post_request(article):
        return api_client.post("/api/articles/", article)

    return send_post_request


@pytest.fixture
def update_article(api_client):
    def send_put_request(article, request_body):
        return api_client.put(f"/api/articles/{article.slug}/", request_body)

    return send_put_request
