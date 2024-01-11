from django.contrib import admin
from inventory.models import Product, Brand, Category, SubCategory, Vendor, SerialNumber

admin.site.register(Vendor)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(SerialNumber)




# Register your models here.
