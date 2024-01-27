from django.shortcuts import render, redirect
from .forms import LoanApplicantForm

def loan_application(request):
    if request.method == 'POST':
        form = LoanApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  # Create a success page or redirect as needed
    else:
        form = LoanApplicantForm()
    return render(request, 'loanproapp/loan_application.html', {'form': form})

def success(request):
    return render(request, 'loanproapp/success.html')
