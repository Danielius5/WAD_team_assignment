from django.shortcuts import render
from django.utils.translation import gettext as _

def user_login(request):
    # for now - just render the login form no matter the type of request
    return render(request, 'booklists/auth/login.html')

def user_register(request):
    # for now - just render the register form no matter the type of request
    return render(request, 'booklists/auth/register.html')

def index(request):
    return render(request, 'booklists/index.html')