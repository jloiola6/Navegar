from django.contrib import admin
from apps.ticket.models import Ticket

# Register your models here.


class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    list_filter = ('user', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    search_fields = ('user', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    readonly_fields = ('user', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    fieldsets = (
        ('Informações do usuário', {
            'fields': ('user', 'origin', 'destination', 'date', 'boat', 'value', 'status')
        }),
    )

admin.site.register(Ticket, TicketAdmin)
