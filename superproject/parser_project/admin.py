from django.contrib import admin

from parser_project.models import Articles
from parser_project.models import Resources


@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "title", "url", "resource")
    list_display_links = ("id", "title")
    search_fields = ("title", "text")
    list_filter = ("resource",)
