from django.shortcuts import render,redirect
from django.utils.translation import gettext as _
from booklists.forms import *
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from booklists.models import *



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
            messages.error(request,user_form.errors)
    else:
        user_form=UserForm
    return render(request, 'booklists/auth/register.html')

def index(request):
    return render(request, 'booklists/index.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('booklists:index'))##change to homepage when ready


def lists_index(request, username):

    created_flag = bool(request.GET.get('created', False))

    if request.method == 'GET':

        lists = List.objects
        if request.user.username != username:
            lists = lists.filter(is_public=True)

        lists = lists.filter(user=User.objects.filter(username=username).first())

        context = {'lists' : lists, 'created' : created_flag, 'username' : username, 'current_user' : request.user}
        return render(request, 'booklists/lists/index.html', context)

@login_required
def lists_create(request, username):

    if request.user.username == username:
        if request.method =='POST':
            lists_create_form=ListForm(request.POST)

            if lists_create_form.is_valid():

                list = lists_create_form.save(commit=False)
                list.user = request.user
                list.save()
                return redirect(reverse('booklists:lists_index', kwargs={'username': username}) + '?created=True')
            else:
                messages.error(request, lists_create_form.errors)

        return render(request, 'booklists/lists/create.html')
    else:
        # unauthorised
        return render(request, 'booklists/errors/401.html', status=401)
