from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.user.models import Cliente, Fornecedor
from django.contrib.auth.models import User


class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ClienteAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Cliente


class FornecedorCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FornecedorAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Fornecedor
