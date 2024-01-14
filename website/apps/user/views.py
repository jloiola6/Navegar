from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from apps.user.forms import *

def index(request):
    return render(request, 'user/index.html')

def signup(request):
    if request.method == 'POST':
        form = ClienteCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('core:index'))
    else:
        form = ClienteCreationForm()
    return render(request, 'user/auth.html', {'form': form, 'auth': 'signup'})

def user_login(request):
    if request.method == 'POST':
        form = ClienteAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('core:index'))
    else:
        form = ClienteAuthenticationForm()
    return render(request, 'user/auth.html', {'form': form, 'auth': 'login'})

def user_logout(request):
    logout(request)
    return redirect(reverse('user:login'))
