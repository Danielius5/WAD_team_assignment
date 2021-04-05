from django.shortcuts import render,redirect
from django.utils.translation import gettext as _
from booklists.forms import UserForm,UserProfileForm
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse




def user_login(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('booklist:index'))
            else:
                return HttpResponse("Your Booklist account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:

        return render(request, 'booklists/auth/login.html')

def user_register(request):
    # for now - just render the register form no matter the type of request
    register=False
    if request.method =='POST':
        user_form=UserForm(request.POST)
        profile_form=UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()

    return render(request, 'booklists/auth/register.html')

def index(request):
    return render(request, 'booklists/index.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('booklist:index'))


