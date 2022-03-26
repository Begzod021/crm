from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, HttpResponse

# Create your views here.


def user_registor(request):
    return render(request, 'Sign Up.html')


def user_login(request):
    return render(request, 'Sign In_.html')
