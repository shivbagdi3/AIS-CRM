from django.db import models
from django.contrib.auth.models import User
    

class Phone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=10)
    

    def __str__(self):
        return f'{self.user.username} - {self.phone_number}'
