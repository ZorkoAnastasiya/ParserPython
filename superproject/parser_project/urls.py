from django.urls import path


app_name = "parse"


def main_page(request):
    from django.http import HttpResponse
    return HttpResponse("Главная страница")


urlpatterns = [
    path('', main_page, name="home"),
]
