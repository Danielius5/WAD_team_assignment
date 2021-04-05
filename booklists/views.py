from django.shortcuts import render,redirect
from django.utils.translation import gettext as _
from booklists.forms import UserForm
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages




def user_login(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                messages.success(request,f"Welcome {username}." )
                return redirect('booklists:index')
            else:
                messages.error(request,("Invalid username or password."))
        else:
            messages.error(request,("Invalid username or password."))


    return render(request, 'booklists/auth/login.html')

def user_register(request):
    registered=False
    if request.method =='POST':
        user_form=UserForm(request.POST)
        if user_form.is_valid():
            user=user_form.save()
            login(request,user)
            return redirect("booklists:index") ## change to homepage when ready
        else:
            messages.error(request,("Username might be taken or password is too short"))
    else:
        user_form=UserForm
        messages.error(request,("Invalid"))
    return render(request, 'booklists/auth/register.html')

def index(request):
    return render(request, 'booklists/index.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('booklists:index'))##change to homepage when ready


