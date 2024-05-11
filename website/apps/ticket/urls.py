from django.urls import path

from apps.ticket.views import *

app_name = 'ticket'

urlpatterns = [
    path('create-ticket/<int:id>/<slug:date>/', create_ticket, name='create_ticket'),
    path('', index, name='index'),
    path('adicionar/<int:id>/<slug:date>/', add, name='add'),
    path('edit/', edit, name='edit'),
    path('<pk>[0-9]/', view, name='view'),
    path('print/<id>[0-9]/', print, name='print'),
]
