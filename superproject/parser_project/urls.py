from django.urls import path
from parser_project.views import NewsListView, AddUrlView, AllResourcesView, ArticlesView

app_name = "parse"

urlpatterns = [
    path('', AllResourcesView.as_view(), name="home"),
    path('add_url/', AddUrlView.as_view(), name="add_url"),
    path('resource/<int:resource_id>', NewsListView.as_view(), name="news_list"),
    path('<int:pk>', ArticlesView.as_view(), name="article"),
]
