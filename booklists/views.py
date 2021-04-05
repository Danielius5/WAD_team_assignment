from django.shortcuts import render,redirect
from django.utils.translation import gettext as _
from booklists.forms import UserForm
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse




def user_login(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(email=email,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('booklist:index'))
            else:
                return HttpResponse("Your Booklist account is disabled")
        else:
            print(f"Invalid login details: {email}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:

        return render(request, 'booklists/auth/login.html')

def user_register(request):
    registered=False
    if request.method =='POST':
        user_form=UserForm(request.POST)
        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            registered=True
        else:
            print(user_form.errors)
    else:
        user_form=UserForm()
    context = {'user_form': user_form,'profile_form': registered}
    return render(request, 'booklists/auth/register.html',context)

def index(request):
    return render(request, 'booklists/index.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('booklist:index'))


