from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("articles", views.ArticleViewSet, basename="articles")

comments_router = routers.NestedDefaultRouter(router, "articles", lookup="article")
comments_router.register("comments", views.CommentViewSet, basename="article-comments")

urlpatterns = router.urls + comments_router.urls
