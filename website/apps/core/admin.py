from django.contrib import admin
from apps.core.models import Utils

# Register your models here.

@admin.register(Utils)
class UtilsAdmin(admin.ModelAdmin):
    list_display = ['discount']
    search_fields = ['discount']

