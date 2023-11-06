from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

class clients(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True, unique=True)
    phone = models.IntegerField(unique=True)
    Alternate_no = models.IntegerField(unique=True, blank=True)
    GST_no = models.CharField(max_length=150, unique=True)
    company_name = models.CharField(max_length=50, blank=True)
    amc_client = models.BooleanField(default=False)
    amc_start_date = models.DateField(null=True, blank=True)
    amc_end_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is being created for the first time
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

@receiver(pre_save, sender=clients)
def set_amc_start_date(sender, instance, **kwargs):
    if instance.amc_client and not instance.amc_start_date:
        # If the client is marked as an AMC client and no start date is set, set the start date to the current date
        instance.amc_start_date = timezone.now().date()
