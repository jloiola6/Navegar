from django.urls import path

from apps.route.views import *

app_name = 'route'

urlpatterns = [
    path('manage-locations', manage_locations, name='manage-locations'),
    path('manage-boats', manage_boats, name='manage-boats'),
    path('manage-routes', manage_routes, name='manage-routes'),
]