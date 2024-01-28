from django.urls import path
from . import views

urlpatterns = [
    path('loan-application/', views.loan_application, name='loan_application'),
    path('success/', views.success, name='success'),
    path('run-script/', views.run_script, name='run_script'),
    path('run-app-js/', views.run_app_js, name='run_app_js'), 
]
