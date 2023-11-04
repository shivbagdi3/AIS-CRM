from django.contrib import admin

from django.contrib import admin
from account.models import Phone
from django.contrib.auth.models import User

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')

admin.site.register(Phone, PhoneAdmin)
