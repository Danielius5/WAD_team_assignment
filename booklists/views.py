from django.shortcuts import render,redirect
from django.utils.translation import gettext as _
from booklists.forms import UserForm
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from booklists.models import User



def user_login(request):
    errors = None
    registered_flag = bool(request.GET.get('registered', False))
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('booklists:index'))
            else:
                errors = "Your Booklist account is disabled"
        else:
            errors = "Invalid login details supplied."

    context = {'errors' : errors, 'registered' : registered_flag}
    return render(request, 'booklists/auth/login.html', context)

def user_register(request):
    errors = None
    if request.method =='POST':
        user_form=UserForm(request.POST)
        if user_form.is_valid():
            if request.POST.get('password') == request.POST.get('password_confirmation'):
                if not User.objects.filter(username=request.POST.get('username')).exists():
                    user=user_form.save()
                    user.set_password(user.password)
                    user.save()
                    return redirect(reverse('booklists:login') + '?registered=True')
                else:
                    errors = "User already exists"
            else:
                errors = "Passwords do not match"
        else:
            errors = user_form.errors
    else:
        user_form=UserForm()

    context = {'user_form': user_form, 'errors' : errors}
    return render(request, 'booklists/auth/register.html',context)

def index(request):
    return render(request, 'booklists/index.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('booklists:index'))


