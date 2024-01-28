import subprocess
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import LoanApplicantForm
from .script import download_images_from_s3
from django.conf import settings

def loan_application(request):
    if request.method == 'POST':
        form = LoanApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success') 
    else:
        form = LoanApplicantForm()
    return render(request, 'loanproapp/loan_application.html', {'form': form})

def success(request):
    return render(request, 'loanproapp/success.html')

def run_script(request):
    if request.method == 'POST':
        download_images_from_s3(settings.AWS_STORAGE_BUCKET_NAME, 'documents/')
        return JsonResponse({'message': 'Script executed successfully'}, status=200)
    return render(request, 'loanproapp/run-script.html')

def run_app_js(request):
    if request.method == 'POST':
        try:

            subprocess.run(['node', 'loanproapp/app.js'], check=True)
            return JsonResponse({'message': 'app.js executed successfully'}, status=200)
        except subprocess.CalledProcessError:
            return JsonResponse({'message': 'Error executing app.js'}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=405)
