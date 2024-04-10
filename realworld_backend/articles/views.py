from rest_framework.viewsets import ModelViewSet

from .models import Article
from .serializers import ArticleSerializer
from .pagination import CustomLimitOffsetPagination


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        queryset = Article.objects.all()

        tag = self.request.query_params.get("tag")
        author = self.request.query_params.get("author")
        favorited_username = self.request.query_params.get("favorited")

        if tag is not None:
            queryset = queryset.filter(tags__name__in=[tag])
        elif author is not None:
            queryset = queryset.filter(author__username=author)
        elif favorited_username is not None:
            queryset = queryset.filter(favorites__user__username=favorited_username)

        return queryset

    def get_serializer_context(self):
        return {"user": self.request.user}
