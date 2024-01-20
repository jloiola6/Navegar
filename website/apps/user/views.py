from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import user_type_required, redirect_authenticated_user


from apps.user.forms import *
from apps.user.models import CustomUser

# @login_required
# @user_type_required('A')
def index(request):
    users = CustomUser.objects.all()
    return render(request, 'user/index.html', {'users': users})


@redirect_authenticated_user
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('core:index'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/auth.html', {'form': form, 'auth': 'signup'})


@redirect_authenticated_user
def user_login(request):
    form = UserAuthenticationForm()
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Use authenticate para verificar as credenciais
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Use login para autenticar o usuário na sessão
                login(request, user)
                return redirect(reverse('core:index'))
            else:
                # Adicione uma mensagem de erro para indicar credenciais inválidas
                form.add_error(None, 'Credenciais inválidas. Por favor, tente novamente.')

    return render(request, 'user/auth.html', {'form': form, 'auth': 'login'})


@login_required
def user_edit(request):
    user = request.user
    form = CustomUserChangeForm(instance=user)

    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=user)
        if form.is_valid():
            if not form.cleaned_data['password']:
                del form.cleaned_data['password']
            
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
                user.save()
            else:
                form.save()

            return redirect(reverse('core:index'))
    return render(request, 'user/auth.html', {'form': form, 'auth': 'edit'})

def user_logout(request):
    logout(request)
    return redirect(reverse('user:login'))
