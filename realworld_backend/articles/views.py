from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Article
from users.models import Follow
from .serializers import ArticleSerializer
from .pagination import CustomLimitOffsetPagination


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = CustomLimitOffsetPagination
    lookup_field = "slug"

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

    @action(detail=False, permission_classes=[IsAuthenticated])
    def feed(self, request):
        queryset = self.get_queryset()
        current_user = self.request.user
        followed_users = Follow.objects.filter(follower=current_user).values_list(
            "following", flat=True
        )
        queryset = queryset.filter(author__in=followed_users)
        serializer = ArticleSerializer(
            queryset, many=True, context={"user": current_user}
        )
        return Response(serializer.data)
