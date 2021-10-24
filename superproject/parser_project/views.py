from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DetailView
from django.contrib.auth import authenticate, login
from parser_project.forms import UserSignupForm, UserLoginForm
from parser_project.models import Articles
from parser_project.parsers import SputnikParserNews, LentaParserNews, EuronewsParserNews


class UserSignupView(SuccessMessageMixin, FormView):
    form_class = UserSignupForm
    template_name = "parser_project/signup.html"
    success_url = reverse_lazy("parse:home")
    success_message = "Вы успешно зарегистрировались!"

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.clean_password2(),
        )
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        message = messages.error(self.request, "Ошибка регистрации!")
        return self.render_to_response(self.get_context_data(form = form, message=message))


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "parser_project/login.html"


class AllResourcesView(ListView):
    model = Articles
    template_name = "parser_project/all_resources.html"
    extra_context = {
        "title": "Новости",
        "header": "Все новости"
    }
    paginate_by = 20


class ResourceNewsView(ListView):
    model = Articles
    template_name = "parser_project/all_resources.html"
    paginate_by = 20

    @staticmethod
    def get_parser(resource):
        if resource == 'Другие ресурсы':
            return
        elif resource == 'Sputnik Беларусь':
            return SputnikParserNews()
        elif resource == 'Lenta Новости':
            return LentaParserNews()
        elif resource == 'Euronews':
            return EuronewsParserNews()

    def save_data(self, news_list):
        pass

    def update_data(self, resource):
        parser = self.get_parser(str(resource.title))
        if parser:
            news_list = parser.get_news_list()
            return self.save_data(news_list)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.model.objects.get(pk=self.kwargs.get('resource_id'))
        context['title'] = obj
        context['header'] = obj
        return context

    def get_queryset(self):
        resource = self.model.objects.get(pk=self.kwargs.get('resource_id'))
        self.update_data(resource)
        return super().get_queryset()


class AddUrlView(CreateView):
    pass


class ArticlesView(DetailView):
    pass
