from django.urls import path

from apps.route.views import *

app_name = 'route'

urlpatterns = [
    path('manage-locations/', manage_locations, name='manage-locations'),
    path('manage-boats/', manage_boats, name='manage-boats'),
    path('', index, name='index'),
    path('edit-route/<int:route_id>/', add_route, name='add-route'),
    path('add-route/', add_route, name='add-route'),
]