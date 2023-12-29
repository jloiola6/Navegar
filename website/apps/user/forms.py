from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.user.models import Cliente, Fornecedor


class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['user__username', 'user__email', 'user__password1', 'user__password2']

class ClienteAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Cliente


class FornecedorCreationForm(UserCreationForm):
    class Meta:
        model = Fornecedor
        fields = ['user__username', 'user__email', 'user__password1', 'user__password2']

class FornecedorAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Fornecedor
