from django.urls import path
from parser_project.views import ResourceNewsView, AddUrlView, AllResourcesView, ArticlesView

app_name = "parse"

urlpatterns = [
    path('', AllResourcesView.as_view(), name="home"),
    path('add_url/', AddUrlView.as_view(), name="add_url"),
    path('resource/<int:resource_id>', ResourceNewsView.as_view(), name= "resource"),
    path('<int:pk>', ArticlesView.as_view(), name="article"),
]
