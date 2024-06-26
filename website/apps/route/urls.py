from django.urls import path

from apps.route.views import *

app_name = 'route'

urlpatterns = [
    path('locais/', locations, name='locations'),
    path('embarcacoes/', boats, name='boats'),
    path('', index, name='index'),
    path('editar/<int:route_id>/', edit_route, name='edit-route'),
    path('adicionar/', add_route, name='add-route'),
]