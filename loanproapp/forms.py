from django import forms
from .models import LoanApplicant

class LoanApplicantForm(forms.ModelForm):
    class Meta:
        model = LoanApplicant
        fields = ['first_name', 'last_name', 'document']
