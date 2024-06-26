from django.contrib import admin
from .models import *

# Register your models here.

class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination')
    list_filter = ('origin', 'destination')
    search_fields = ('origin', 'destination')

class BoatAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_filter = ('name', 'supplier')
    search_fields = ('name', 'supplier')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class RouteWeekdayAdmin(admin.ModelAdmin):
    list_display = ('route', 'weekday', 'boat')
    list_filter = ('route', 'weekday', 'boat')
    search_fields = ('route', 'weekday', 'boat')

class RouteDiscountAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'route', 'discounted_value', 'discounted_cost', 'is_active')


admin.site.register(Route, RouteAdmin)
admin.site.register(Boat, BoatAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(RouteWeekday, RouteWeekdayAdmin)
admin.site.register(RouteDiscount, RouteDiscountAdmin)