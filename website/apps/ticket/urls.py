from django.urls import path

from apps.ticket.views import *

app_name = 'ticket'

urlpatterns = [
    path('create-ticket/<int:id>/<slug:date>/', create_ticket, name='create_ticket'),
    path('index/', index, name='index'),
    path('add/<int:id>/<slug:date>/', add, name='add'),
    path('edit/', edit, name='edit'),
    path('view/<int:pk>/', view, name='view'),
    path('print/<int:id>/', print, name='print'),
]
