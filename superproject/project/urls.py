from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from parser_project.views import UserSignupView, UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserSignupView.as_view(), name="signup"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name= "logout"),
    path('parse/', include('parser_project.urls')),
]
