from django.urls import path
from parser_project.views import ResourceNewsView, AddUrlView, AllResourcesView, DeleteUrlView
from parser_project.views import ArticlesView, UserArchiveView, AddArticleArchiveView
from parser_project.views import DeleteArticleArchiveView, UpdateArticleView

app_name = "parse"

urlpatterns = [
    path('', AllResourcesView.as_view(), name="home"),
    path('add_url/', AddUrlView.as_view(), name="add_url"),
    path('archive/', UserArchiveView.as_view(), name="archive"),
    path('resource/<int:resource_id>', ResourceNewsView.as_view(), name= "resource"),
    path('<int:pk>', ArticlesView.as_view(), name="article"),
    path('<int:pk>/add_archive', AddArticleArchiveView.as_view(), name= "add_archive"),
    path('<int:pk>/delete_archive', DeleteArticleArchiveView.as_view(), name= "delete_archive"),
    path('<int:pk>/delete_url', DeleteUrlView.as_view(), name= "delete_url"),
    path('<int:pk>/update', UpdateArticleView.as_view(), name= "update"),
]
