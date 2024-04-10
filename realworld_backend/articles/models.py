from django.db import models
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager


User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    body = models.TextField()
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name="favorites", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "article"], name="unique favorite")
        ]

    def __str__(self) -> str:
        return self.article.title

    def username(self):
        return self.user.username
