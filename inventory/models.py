from collections.abc import Iterable
from django.db import models
from client.models import clients
import uuid


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255)

    def __str__(self):
        return self.vendor_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.subcategory_name    


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    model_name = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)  
    
    def __str__(self):
        return self.name

class SerialNumber(models.Model):
    serial_number = models.CharField(max_length=50, unique=True)
    CHOICES = [
        ('S', 'Sold'),
        ('NS', 'Not Sold'),
    ]
    status = models.CharField(max_length=2, choices=CHOICES, default='NS')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='serialnumber')
    in_date = models.DateField(blank=True)
    update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.serial_number} - {self.get_status_display()}"
    

        