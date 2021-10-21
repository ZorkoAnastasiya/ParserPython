from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, ListView, DetailView
from django.contrib.auth import authenticate, login
from parser_project.forms import UserSignupForm, UserLoginForm


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


class NewsListView(View):
    pass


class AddUrlView(CreateView):
    pass


class AllResourcesView(ListView):
    pass


class ArticlesView(DetailView):
    pass
