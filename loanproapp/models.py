# loanproapp/models.py
from django.db import models

class LoanApplicant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')  # Local testing
    date_of_birth = models.DateField()
    email = models.EmailField()
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    loan_amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    purpose_of_loan = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
