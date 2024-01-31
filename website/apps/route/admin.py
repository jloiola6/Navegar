from django.contrib import admin
from .models import *

# Register your models here.

class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination')
    list_filter = ('origin', 'destination')
    search_fields = ('origin', 'destination')


class BoatAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('name', 'user')
    search_fields = ('name', 'user')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class RouteWeekdayAdmin(admin.ModelAdmin):
    list_display = ('route', 'weekday', 'boat')
    list_filter = ('route', 'weekday', 'boat')
    search_fields = ('route', 'weekday', 'boat')


admin.site.register(Route, RouteAdmin)
admin.site.register(Boat, BoatAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(RouteWeekday, RouteWeekdayAdmin)