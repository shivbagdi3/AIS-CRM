from django.contrib import admin
from client.models import clients
from django import forms





# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','company_name', 'amc_client', 'amc_start_date', 'amc_end_date', 'email', 'phone')
    list_filter = ('amc_client',)  # Add more filters as needed
    search_fields = ('company_name', 'email', 'phone')  # Add more fields as needed

admin.site.register(clients, ClientAdmin)
