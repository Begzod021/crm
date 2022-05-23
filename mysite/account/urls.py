"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('register/<str:username>/', user_registor, name='user_registor'),
    path('', user_login, name='user_login'),
    path('logout/', logout_user, name='logout'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('employe/<str:username>/', employe, name='employe'),
    path('404/<str:username>/', error_404, name='error'),
    path('505-erorrs/<str:username>/', error_500, name='erorr_505'),
    path('user-tablets/<str:username>/', user_tablets, name='user_tablets'),
    path('delete-employe/<str:username>/', delete_employe, name='delete-employe'),
    path('change-password/<str:username>/', change_password, name='change_password'),
    path('edit-employe/<str:username>/', edit_profile, name='edit_profile'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="account/passwor_reset_done.html"), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/new_password.html"), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/reset_password_complete.html"), name="password_reset_complete")
]
