from django.db import models
from django.utils import timezone

 #Create your models here.
class clients(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100, blank=True)
	phone = models.IntegerField(unique=True)
	Alternate_no =  models.IntegerField(unique=True, blank=True)
	GST_no =  models.CharField(max_length=150, unique=True)
	company_name = models.CharField(max_length=50, blank=True)
	amc_client = models.BooleanField(default=False)
	updated_at = models.DateTimeField(auto_now_add=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.pk:  # Check if the object is being created for the first time
			self.created_at = timezone.now()
		super().save(*args, **kwargs)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")
	


