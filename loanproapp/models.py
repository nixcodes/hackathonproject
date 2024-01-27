from django.db import models

# Create your models here.

from django.db import models

class LoanApplicant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')
