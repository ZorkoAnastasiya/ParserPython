from django.urls import path

from parser_project.views import AddArticleArchiveView
from parser_project.views import AddUrlView
from parser_project.views import AllResourcesView
from parser_project.views import ArticlesView
from parser_project.views import DeleteArticleArchiveView
from parser_project.views import ResourceNewsView
from parser_project.views import UpdateArticleView
from parser_project.views import UserArchiveView

app_name = "parse"

urlpatterns = [
    path("", AllResourcesView.as_view(), name="home"),
    path("add_url/", AddUrlView.as_view(), name="add_url"),
    path("archive/", UserArchiveView.as_view(), name="archive"),
    path(
        "resource/<int:resource_id>",
        ResourceNewsView.as_view(),
        name="resource",
    ),
    path("<int:pk>", ArticlesView.as_view(), name="article"),
    path(
        "<int:pk>/add_archive",
        AddArticleArchiveView.as_view(),
        name="add_archive",
    ),
    path(
        "<int:pk>/delete_archive",
        DeleteArticleArchiveView.as_view(),
        name="delete_archive",
    ),
    path("<int:pk>/update", UpdateArticleView.as_view(), name="update"),
]
