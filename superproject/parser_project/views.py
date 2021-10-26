from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DetailView, RedirectView
from django.contrib.auth import authenticate, login
from parser_project.forms import UserSignupForm, UserLoginForm, AddUrlForm
from parser_project.models import Articles, Resources, User
from parser_project.parsers import SputnikParserNews, LentaParserNews, EuronewsParserNews, UniversalParser
from datetime import datetime


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


class AllResourcesView(LoginRequiredMixin, ListView):
    model = Articles
    template_name = "parser_project/all_resources.html"
    extra_context = {
        "title": "Новости",
        "header": "Все новости"
    }
    paginate_by = 20


class ResourceNewsView(LoginRequiredMixin, ListView):
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

    def save_data_list(self, news_list, pk):
        for item in news_list:
            if not self.model.objects.filter(url=item['url']).exists():
                self.model.objects.create(
                    date = item['date'],
                    title = item['title'],
                    url = item['url'],
                    resource_id = pk
                )

    def parse_news_list(self, pk):
        obj = Resources.objects.get(id=pk)
        parser = self.get_parser(str(obj.title))
        if parser:
            news_list = parser.get_news_list()
            if news_list:
                return self.save_data_list(news_list, pk)

    def get_queryset(self):
        pk = self.kwargs.get('resource_id')
        self.parse_news_list(pk)
        return super().get_queryset().filter(resource_id=pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Resources.objects.get(pk=self.kwargs.get('resource_id'))
        context['title'] = obj
        context['header'] = obj
        return context


class UserArchiveView(LoginRequiredMixin, ListView):
    model = Articles
    template_name = "parser_project/all_resources.html"
    paginate_by = 20
    extra_context = {
        "title": "Мой Архив",
        "header": "Мой Архив"
    }

    def get_queryset(self):
        user = self.request.user.id
        return super().get_queryset().filter(users=user)


class ArticlesView(LoginRequiredMixin, DetailView):
    model = Articles
    template_name = "parser_project/article.html"

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

    def save_data_text(self, text, pk):
        obj = self.model.objects.get(id = pk)
        obj.date = text['date']
        obj.text = text['text']
        obj.save()

    def parse_text(self, obj):
        parser = self.get_parser(str(obj.resource.title))
        if parser:
            url = obj.url
            text = parser.get_news_text(url)
            if text:
                return self.save_data_text(text, obj.id)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        obj = self.model.objects.get(id = pk)
        if not obj.text:
            self.parse_text(obj)
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.model.objects.get(id = self.kwargs.get('pk')).users.all()
        for user in obj:
            if self.request.user.id == user.id:
                context['archive'] = self.request.user.id
        context['header'] = "Статья"
        return context


class AddArticleArchiveView(LoginRequiredMixin, RedirectView):
    pattern_name = "parse:article"

    def get_redirect_url(self, *args, **kwargs):
        obj = Articles.objects.get(id = self.kwargs.get('pk'))
        obj.users.add(self.request.user.id)
        return super().get_redirect_url(*args, **kwargs)


class DeleteArticleArchiveView(LoginRequiredMixin, RedirectView):
    pattern_name = "parse:article"

    def get_redirect_url(self, *args, **kwargs):
        obj = Articles.objects.get(id=self.kwargs.get('pk'))
        user = User.objects.get(id=self.request.user.id)
        user.articles_set.remove(obj)
        return super().get_redirect_url(*args, **kwargs)


class UpdateArticleView(LoginRequiredMixin, RedirectView):
    model = Articles
    pattern_name = "parse:article"

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

    def save_data_text(self, text, pk):
        obj = self.model.objects.get(id = pk)
        obj.date = text['date']
        obj.text = text['text']
        obj.save()

    def parse_text(self, obj):
        parser = self.get_parser(str(obj.resource.title))
        if parser:
            url = obj.url
            text = parser.get_news_text(url)
            if text:
                return self.save_data_text(text, obj.id)

    def get_redirect_url(self, *args, **kwargs):
        obj = self.model.objects.get(id = self.kwargs.get('pk'))
        self.parse_text(obj)
        return super().get_redirect_url(*args, **kwargs)


class AddUrlView(LoginRequiredMixin, CreateView):
    form_class = AddUrlForm
    template_name = "parser_project/add_url.html"
    extra_context = {"title": "Добавить ссылку", "header": "Новая ссылка"}
    login_url = "parse:article"

    def form_valid(self, form):
        obj = form.save(commit = False)
        parser = UniversalParser()
        article = parser.parse_html(obj.url)
        res = Resources.objects.get(title = "Другие ресурсы")
        obj.resource_id = res.id
        if article:
            obj.date = article["date"]
            obj.title = article["title"]
            obj.url = article["url"]
            obj.text = article["text"]
        else:
            obj.date = datetime.today()
            obj.title = "Информация не найдена"
            obj.text = "Попробуйте обновить данные позже"
        obj.save()
        return super().form_valid(form)
