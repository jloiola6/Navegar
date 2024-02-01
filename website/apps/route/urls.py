from django.urls import path

from apps.route.views import *

app_name = 'route'

urlpatterns = [
    path('manage-locations/', manage_locations, name='manage-locations'),
    path('manage-boats/', manage_boats, name='manage-boats'),
    path('manage-routes/', manage_routes, name='manage-routes'),
    path('edit-route/<int:route_id>/', add_route, name='add-route'),
    path('add-route/', add_route, name='add-route'),
]