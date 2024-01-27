from django.urls import path
from .views import loan_application, success

urlpatterns = [
    path('loan_application/', loan_application, name='loan_application'),
    path('success/', success, name='success'),
    # Add more URL patterns as your project evolves
]
