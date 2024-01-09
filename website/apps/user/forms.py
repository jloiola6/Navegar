from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.user.models import Cliente, Fornecedor
from django.contrib.auth.models import User


class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Uusário',
            'email': 'Email',
            'password1': 'Senha',
            'password2': 'Senha (Novamente)',
        }

class ClienteAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Usuário',
            'email': 'Email',
            'password1': 'Senha',
            'password2': 'Senha (Novamente)',
        }


class FornecedorCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Uusário',
            'email': 'Email',
            'password1': 'Senha',
            'password2': 'Senha (Novamente)',
        }

class FornecedorAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Fornecedor
