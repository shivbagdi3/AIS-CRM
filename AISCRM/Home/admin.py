from django.contrib import admin
from .models import EmailAddress, contactus

class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ['email']
    search_fields = ['email']
    list_per_page = 25

class contactusAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    search_fields = ['name']
    list_per_page = 25


admin.site.register(EmailAddress, EmailAddressAdmin)
admin.site.register(contactus, contactusAdmin)
