from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, HttpResponse

# Create your views here.


def user_registor(request):
    return render(request, 'SignUp.html')


def user_login(request):
    return render(request, 'SignIn.html')
