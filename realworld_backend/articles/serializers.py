from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from .models import Article
from users.serializers import ProfileSerializer


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = ProfileSerializer()
    tags = TagListSerializerField()
    favorited = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()

    def get_favorited(self, article):
        user = self.context.get("user")
        if user.is_authenticated:
            return article.favorites.filter(user=user).exists()
        return False

    def get_favorites_count(self, article):
        return article.favorites.count()

    class Meta:
        model = Article
        fields = (
            "slug",
            "title",
            "description",
            "body",
            "tags",
            "created_at",
            "updated_at",
            "favorited",
            "favorites_count",
            "author",
        )
