from django.urls import path
from .views import *

urlpatterns = [
    path('api-register/',UserRegister.as_view(), name='api-register'),
    path('api-get/<str:username>/', GetEmploye.as_view(), name='get-api'),
    path('api-employe/<str:username>/', RegisterEmploye.as_view(), name='api-employe'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('director-profile/', DirectorProfile.as_view(), name='profile-director'),
    path('worker-profile/', worker_profile, name='profile-worker'),
    path('worker-profiles/', WorkerProfile.as_view(), name='worker-profile')
]