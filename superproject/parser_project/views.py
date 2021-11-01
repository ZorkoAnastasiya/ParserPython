from django.contrib import messages
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from parser_project.forms import UserSignupForm, UserLoginForm, AddUrlForm
from parser_project.models import Articles, Resources, User
from parser_project.parser.universal import UniversalParser
from parser_project.utils import ParserMixin
from django.views.generic import FormView, CreateView, ListView, DetailView, RedirectView, DeleteView


class UserSignupView(SuccessMessageMixin, FormView):
    """
    User registration.
    """
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
    """
    User authorization.
    """
    form_class = UserLoginForm
    template_name = "parser_project/login.html"


class AllResourcesView(LoginRequiredMixin, ListView):
    """
    Presentation of all news from all resources.
    """
    model = Articles
    template_name = "parser_project/all_resources.html"
    extra_context = {
        "title": "Новости",
        "header": "Все новости"
    }
    paginate_by = 20


class ResourceNewsView(LoginRequiredMixin, ParserMixin, ListView):
    """
    Presentation of news from only one specific resource.
    """
    model = Articles
    template_name = "parser_project/all_resources.html"
    paginate_by = 20

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
    """
    Submission of only articles saved by the user to the archive.
    """
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


class ArticlesView(LoginRequiredMixin, ParserMixin, DetailView):
    """
    Submission of one specific article.
    """
    model = Articles
    template_name = "parser_project/article.html"

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.model, id = pk)
        if not obj.text:
            self.parse_text(obj)
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.model.objects.get(id = self.kwargs.get('pk')).users.all()
        for user in obj:
            if self.request.user.id == user.id:
                context['archive'] = self.request.user.id
        obj = self.model.objects.get(id = self.kwargs.get('pk'))
        if self.request.user.id == obj.owner_id:
            context['owner'] = self.request.user.id
        context['header'] = "Статья"
        return context


class AddArticleArchiveView(LoginRequiredMixin, RedirectView):
    """
    Adding an article to the archive.
    """
    pattern_name = "parse:article"

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Articles, id = self.kwargs.get('pk'))
        obj.users.add(self.request.user.id)
        return super().get_redirect_url(*args, **kwargs)


class DeleteArticleArchiveView(LoginRequiredMixin, RedirectView):
    """
    Removing an article from the archive.
    """
    pattern_name = "parse:article"

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Articles, id=self.kwargs.get('pk'))
        user = User.objects.get(id=self.request.user.id)
        user.articles_set.remove(obj)
        return super().get_redirect_url(*args, **kwargs)


class UpdateArticleView(LoginRequiredMixin, ParserMixin, RedirectView):
    """
    Updating the article. Re-parsing the HTML page.
    """
    model = Articles
    pattern_name = "parse:article"

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(self.model, id = self.kwargs.get('pk'))
        if str(obj.resource.title) != "Другие ресурсы":
            self.parse_text(obj)
        else:
            parser = UniversalParser()
            article = parser.parse_html(obj.url)
            if article:
                obj.date = article["date"]
                obj.title = article["title"]
                obj.text = article["text"]
                obj.save()
        return super().get_redirect_url(*args, **kwargs)


class AddUrlView(LoginRequiredMixin, CreateView):
    """
    Adding a user link and parsing the HTML page at the specified address.
    Saving the received data.
    """
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
        obj.owner = self.request.user
        if article:
            obj.date = article["date"]
            obj.title = article["title"]
            obj.url = article["url"]
            obj.text = article["text"]
        else:
            obj.date = datetime.today()
            obj.title = "Информация не найдена"
            obj.text = "Попробуйте обновить данные позже или перейти на источник"
        obj.save()
        return super().form_valid(form)


class DeleteUrlView(LoginRequiredMixin, DeleteView):
    model = Articles
    template_name = "parser_project/delete_url.html"
    success_url = reverse_lazy("parse:home")
    login_url = "parse:article"

    def get_queryset(self):
        return super().get_queryset().filter(id = self.kwargs.get('pk'))
