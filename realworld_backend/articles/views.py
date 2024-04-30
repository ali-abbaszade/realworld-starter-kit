from django.utils.text import slugify

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from .models import Article, Comment
from users.models import Follow
from .serializers import ArticleSerializer, CommentSerializer
from .pagination import CustomLimitOffsetPagination


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.data.get("title"):
            title = request.data["title"]
            slug = slugify(title)
            instance.slug = slug

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

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


class CommentViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(article__slug=self.kwargs["article_slug"])

    def get_serializer_context(self):
        article = Article.objects.get(slug=self.kwargs["article_slug"])
        return {
            "article_id": article.id,
            "author_id": self.request.user.id,
            "user": self.request.user,
        }

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except:
            return Response(
                "You submitted a comment for this article.",
                status=status.HTTP_400_BAD_REQUEST,
            )
