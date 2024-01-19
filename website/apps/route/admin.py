from django.contrib import admin
from .models import *

# Register your models here.

class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'weekday', 'boat')
    list_filter = ('origin', 'destination', 'weekday', 'boat')
    search_fields = ('origin', 'destination', 'weekday', 'boat')


class BoatAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    list_filter = ('name', 'capacity')
    search_fields = ('name', 'capacity')


admin.site.register(Route, RouteAdmin)
admin.site.register(Boat, BoatAdmin)