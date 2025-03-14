from django.contrib import admin
from support.models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('status', 'title', 'user', 'created_date')
    list_filter = ("status","user","created_date")
    search_fields = ['title', 'body']
admin.site.register(Ticket, TicketAdmin)

