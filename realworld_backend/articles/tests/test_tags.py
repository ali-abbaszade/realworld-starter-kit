from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker

import pytest
from taggit.models import Tag


@pytest.mark.django_db
def test_list_tags_returns_200():
    tags = baker.make(Tag, _quantity=5)

    client = APIClient()
    response = client.get("/api/tags/")

    assert response.status_code == status.HTTP_200_OK
