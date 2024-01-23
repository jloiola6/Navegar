from django.urls import path

from apps.ticket.views import *

app_name = 'ticket'

urlpatterns = [
    path('create-ticket/<int:id>/<slug:date>', create_ticket, name='create_ticket'),
    path('index/', index, name='index'),
    path('add/<int:id>/<slug:date>', add, name='add'),
]