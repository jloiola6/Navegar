from django.contrib import admin
from apps.ticket.models import Ticket

# Register your models here.


class TicketAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_create', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    list_filter = ('created_at', 'user_create', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    search_fields = ('created_at', 'user_create', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    # readonly_fields = ('user_create', 'origin', 'destination', 'date', 'boat', 'value', 'document', 'status')
    # fieldsets = (
    #     ('Informações do usuário', {
    #         'fields': ('user_create', 'origin', 'destination', 'date', 'boat', 'value', 'document', 'status')
    #     }),
    # )

admin.site.register(Ticket, TicketAdmin)
