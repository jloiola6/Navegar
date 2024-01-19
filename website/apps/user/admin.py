from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser as User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'phone', 'type')
    list_filter = ('type')
    search_fields = ('username', 'email', 'name', 'phone')
    ordering = ('username',)

admin.site.register(User)