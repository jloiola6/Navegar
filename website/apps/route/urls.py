from django.urls import path

from apps.route.views import *

app_name = 'route'

urlpatterns = [
    path('locais/', locations, name='locations'),
    path('embarcacoes/', boats, name='boats'),
    path('', index, name='index'),
    path('edit-route/<int:route_id>/', add_route, name='add-route'),
    path('add-route/', add_route, name='add-route'),
]