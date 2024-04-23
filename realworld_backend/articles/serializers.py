from django.utils.text import slugify
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from .models import Article
from users.serializers import ProfileSerializer


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    tags = TagListSerializerField()
    favorited = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)

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

    def create(self, validated_data):
        user = self.context.get("user")
        title = validated_data["title"]
        slug = slugify(title)
        tags = validated_data.pop("tags")
        instance = Article.objects.create(author=user, slug=slug, **validated_data)
        instance.tags.add(*tags)
        return instance
