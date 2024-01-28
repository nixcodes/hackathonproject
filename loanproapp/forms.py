# forms.py
from django import forms
from .models import LoanApplicant

class LoanApplicantForm(forms.ModelForm):
    class Meta:
        model = LoanApplicant
        fields = '__all__'

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'border rounded-md p-2'}),
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'border rounded-md p-2'}),
    )
    document = forms.FileField(
        label='Document',
        widget=forms.ClearableFileInput(attrs={'class': 'border rounded-md p-2'}),
    )
    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'class': 'border rounded-md p-2'}),
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'border rounded-md p-2'}),
    )
    monthly_income = forms.DecimalField(
        label='Monthly Income',
        widget=forms.NumberInput(attrs={'class': 'border rounded-md p-2'}),
    )
    loan_amount_requested = forms.DecimalField(
        label='Loan Amount Requested',
        widget=forms.NumberInput(attrs={'class': 'border rounded-md p-2'}),
    )
    purpose_of_loan = forms.CharField(
        label='Purpose of Loan',
        widget=forms.Textarea(attrs={'class': 'border rounded-md p-2'}),
    )
