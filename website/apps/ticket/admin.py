from django.contrib import admin
from apps.ticket.models import Ticket

# Register your models here.


class TicketAdmin(admin.ModelAdmin):
    list_display = ('user_create', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    list_filter = ('user_create', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    search_fields = ('user_create', 'origin', 'destination', 'date', 'boat', 'value', 'status')
    # readonly_fields = ('user_create', 'origin', 'destination', 'date', 'boat', 'value', 'document', 'status')
    # fieldsets = (
    #     ('Informações do usuário', {
    #         'fields': ('user_create', 'origin', 'destination', 'date', 'boat', 'value', 'document', 'status')
    #     }),
    # )

admin.site.register(Ticket, TicketAdmin)
