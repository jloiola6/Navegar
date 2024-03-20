from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = "Nome completo"
        self.fields['email'].widget.attrs['placeholder'] = "E-mail"
        self.fields['phone'].widget.attrs['placeholder'] = "Telefone"
        self.fields['phone'].widget.attrs['required'] = "true"
        self.fields['password1'].widget.attrs['placeholder'] = "Senha"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirmação da senha"

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone','password1', 'password2']

class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'cpf', 'phone']

class UserAuthenticationForm(AuthenticationForm):
    phone = forms.CharField(
        label=("Telefone"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "email-input"
        self.fields['username'].widget.attrs['placeholder'] = "E-mail"
        self.fields['username'].required = False

        self.fields['phone'].widget.attrs['placeholder'] = "Telefone"
        self.fields['phone'].required = False

        self.fields['password'].widget.attrs['class'] = "password-input"
        self.fields['password'].widget.attrs['placeholder'] = "Senha"
        self.fields['password'].widget.attrs['maxlength'] = "128"

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password']

