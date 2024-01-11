from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python
from django.contrib.auth.models import User

class clients(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True, unique=True)
    phone = PhoneNumberField(default='')
    Alternate_no = PhoneNumberField(default='')
    GST_no = models.CharField(max_length=150, unique=True)
    company_name = models.CharField(max_length=50, blank=True)
    amc_client = models.BooleanField(default=False)
    amc_start_date = models.DateField(null=True, blank=True)
    amc_end_date = models.DateField(null=True, blank=True)

    def remaining_days(self):
        today = timezone.now().date()
        remaining_days = (self.amc_end_date - today).days
        return remaining_days

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class update_at(models.Model):
    update_id = models.ForeignKey(clients, on_delete=models.CASCADE, related_name='update_at')
    update = models.DateField(blank=True)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='by_user')


class Feedback(models.Model):
    feedback_id = models.ForeignKey(clients, on_delete=models.CASCADE, related_name='feedback_id')
    feed_back = models.CharField(max_length=1000, blank= True)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_by')

    def __str__(self):
        return self.feed_back
