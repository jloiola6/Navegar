from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Cliente, Fornecedor

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class ClienteCreationForm(CustomUserCreationForm):
    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password1', 'password2']

class ClienteAuthenticationForm(CustomUserAuthenticationForm):
    class Meta:
        model = Cliente

class FornecedorCreationForm(CustomUserCreationForm):
    class Meta:
        model = Fornecedor
        fields = ['username', 'email', 'password1', 'password2']

class FornecedorAuthenticationForm(CustomUserAuthenticationForm):
    class Meta:
        model = Fornecedor