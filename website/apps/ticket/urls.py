from django.urls import path

from apps.ticket.views import *

app_name = 'ticket'

urlpatterns = [
    path('create-ticket', create_ticket, name='create_ticket'),
]