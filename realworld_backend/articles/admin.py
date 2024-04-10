from django.contrib import admin

from .models import Article, Favorite


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    autocomplete_fields = ["author"]
    list_display = ["title", "author", "created_at"]
    search_fields = ["title", "description"]
    list_per_page = 10


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["article", "username"]
