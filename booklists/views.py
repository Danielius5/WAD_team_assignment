from django.shortcuts import render,redirect
from django.utils.translation import gettext as _
from booklists.forms import UserForm,CommentForm
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Book,Comment,Rating




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

def show_book(request,book_name_slug):
    context_dict={}
    print(book_name_slug)
    try:
        book=Book.objects.get(slug=book_name_slug)
        context_dict['book']=book
    except Book.DoesNotExist:
        context_dict['book']=None

    try:
        comments=Comment.objects.filter(book=book)
        context_dict['comments']=comments
    except Comment.DoesNotExist:
        context_dict['comments']=None
   # try:
   #     rating=Rating.objects.filter(book=book)
   #     counter=0
   #     total=0
   #     for star in rating:
   ##         total+=star.rating
   #         counter+=1
#
    #    total/=counter
    #    context_dict['rating']=total
   # except Rating.DoesNotExist:
   #     context_dict['rating']=None
    
    if request.method == 'POST':
        comment=request.POST['comment']

        comment_form=CommentForm({'comment':comment,'book':book,'user':request.user})
        print(comment)

        if comment_form.is_valid():
            comment_form.save()
        else:   
            print('fail')

    comment_form=CommentForm()        
    context_dict['user']=request.user
    return render(request, 'booklists/book.html',context=context_dict)
