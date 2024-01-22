from django.urls import path

from apps.user.views import *

app_name = 'user'

urlpatterns = [
    path('', index, name='index'),

    path('login/', user_login, name='login'),
    path('edi/t', user_edit, name='edit'),
    path('cadastro/', signup, name='signup'),
    path('logout/', user_logout, name='logout'),
]