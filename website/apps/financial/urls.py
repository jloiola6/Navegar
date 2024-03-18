from django.urls import path

from apps.financial.views import *

app_name = 'financial'

urlpatterns = [
    path('', index, name='index'),
]