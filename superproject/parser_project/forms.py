from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from parser_project.models import User, Articles


class AddUrlForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ["url"]
        widgets = {"url": forms.URLInput(attrs = {"class": "form-control"})}


class UserSignupForm(UserCreationForm):
    username = forms.CharField(
        label = "Пользователь",
        widget = forms.TextInput(attrs = {"class": "form-control"})
    )
    email = forms.EmailField(
        label = "Email адрес",
        widget = forms.EmailInput(attrs = {"class": "form-control"})
    )
    password1 = forms.CharField(
        label = "Пароль",
        widget =forms.PasswordInput(attrs = {"class": "form-control"})
    )
    password2 = forms.CharField(
        label = "Подтверждение пароля",
        widget =forms.PasswordInput(attrs = {"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label = "Имя Пользователя",
        widget = forms.TextInput(attrs = {"class": "form-control"})
    )
    password = forms.CharField(
        label = "Пароль",
        widget = forms.PasswordInput(attrs = {"class": "form-control"})
    )
