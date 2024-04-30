from django.utils.text import slugify
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from .models import Article, Comment
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


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "created_at", "updated_at", "body", "author")

    def create(self, validated_data):
        article_id = self.context["article_id"]
        author_id = self.context["author_id"]
        return Comment.objects.create(
            article_id=article_id, author_id=author_id, **validated_data
        )
