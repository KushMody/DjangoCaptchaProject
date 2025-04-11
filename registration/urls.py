# registration/urls.py

from django.urls import path
from .views import congrats,register, success, user_login  # Import views

urlpatterns = [
    path('register/', register, name='register'),  # URL for the registration view
    path('success/', success, name='success'),     # URL for the success view
    path('login/', user_login, name='login'),      # URL for the login view
    path('congrats/', congrats, name='congrats'),
]
