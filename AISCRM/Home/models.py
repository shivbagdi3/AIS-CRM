from django.db import models

class EmailAddress(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class contactus(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, unique=True)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.name
