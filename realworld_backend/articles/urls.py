from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("articles", views.ArticleViewSet, basename="articles")

comments_router = routers.NestedDefaultRouter(router, "articles", lookup="article")
comments_router.register("comments", views.CommentViewSet, basename="article-comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(comments_router.urls)),
    path("tags/", views.TagList.as_view()),
]
