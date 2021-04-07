from django.shortcuts import render,redirect
from django.utils.translation import gettext as _
from booklists.forms import *
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from booklists.models import *
import json
from django.db.models import Q

def user_login(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('booklists:index')

def user_register(request):
    registered=False
    if not request.user.is_authenticated:
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
    else:
        return redirect('booklists:index')

def index(request):
    return render(request, 'booklists/index.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('booklists:index'))##change to homepage when ready

def show_book(request,book_name_slug):
    context_dict={}
    try:
        book=Book.objects.get(slug=book_name_slug)
        context_dict['book']=book

    except Book.DoesNotExist:
        return render(request, 'booklists/errors/404.html', status=404)

    comments=Comment.objects.filter(book=book)
    context_dict['comments']=comments
    
    if request.method == 'POST':
        comment=request.POST['comment']

        comment_form=CommentForm({'comment':comment,'book':book,'user':request.user})
        print(comment)

        if comment_form.is_valid():
            comment_form.save()
        else:   
            print('fail')
    lists = []
    if request.user.is_authenticated:
        lists = List.objects.filter(user=request.user)

    context_dict['lists'] = lists

    context_dict['user']=request.user
    return render(request, 'booklists/books/view.html',context=context_dict)

def lists_index(request, username):

    created_flag = bool(request.GET.get('created', False))
    edited_flag = bool(request.GET.get('edited', False))
    deleted_flag = bool(request.GET.get('deleted', False))
    user = User.objects.filter(username=username).first()
    if user:
        if request.method == 'GET':

            lists = List.objects
            if request.user.username != username:
                lists = lists.filter(is_public=True)

            lists = lists.filter(user=User.objects.filter(username=username).first())

            context = {'lists' : lists, 'created' : created_flag, 'username' : username, 'current_user' : request.user, 'edited' : edited_flag, 'deleted' : deleted_flag}
            return render(request, 'booklists/lists/index.html', context)
    else:
        return render(request, 'booklists/errors/404.html', status=404)


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

@login_required
def lists_edit(request, username, list_slug):

    if request.user.username == username:
        current_data = List.objects.filter(slug=list_slug).first()

        if not current_data is None:

            if request.method =='POST':
                lists_create_form=ListForm(request.POST or None, instance=current_data)
                if lists_create_form.is_valid():
                    lists_create_form.save()
                    return redirect(reverse('booklists:lists_index', kwargs={'username': username}) + '?edited=True')
                else:
                    messages.error(request, lists_create_form.errors)

            return render(request, 'booklists/lists/edit.html', context={'current_data' : current_data, 'username' : username})

        else:
            # not found
            return render(request, 'booklists/errors/404.html', status=404)
    else:
        # unauthorised
        return render(request, 'booklists/errors/401.html', status=401)

def lists_view(request, username, list_slug):

    added_flag = bool(request.GET.get('added', False))
    deleted_flag = bool(request.GET.get('deleted', False))

    current_list = List.objects.filter(slug=list_slug).first()
    books = current_list.books.all()

    lists = []
    # used for add to button
    if request.user.is_authenticated:
        lists = List.objects.filter(user=request.user)

    if not current_list is None:

        if request.user.is_authenticated:
            # only care about user ratings for "star" rating
            for book in books:
                book.my_rating = book.rating_set.filter(user=request.user).first()

        context = {'current_list': current_list, 'books' : books, 'lists' : lists,
                    'username': username, 'user': request.user, 'added' : added_flag, 'deleted': deleted_flag}

        return render(request, 'booklists/lists/view.html', context)
    else:

        # not found
        return render(request, 'booklists/errors/404.html', status=404)


@login_required
def book_rate(request, book_slug):
    rating = request.POST.get('rating')
    if request.method == 'POST':
        rating = int(rating)

        if 1 <= rating <= 5:

            book = Book.objects.filter(slug=book_slug).first()

            if not book is None:
                user_rating = Rating.objects.filter(user=request.user, book=book).first()

                # already rated, change
                if user_rating:

                    book.average_rating = ((book.average_rating * book.ratings_count) - user_rating.rating + rating) / book.ratings_count
                    book.save()
                    user_rating.rating = rating
                    user_rating.save()

                # new user rates
                else:
                    user_rating = Rating.objects.create(user=request.user, book=book, rating=rating)
                    # floatint point erors should be small enough to not be noticed
                    # should be much more efficient than recounting ratings

                    # avoiding 0 division
                    if book.ratings_count < 1:
                        book.average_rating = rating
                    else:
                        book.average_rating = ( (book.average_rating * book.ratings_count) + rating ) / ( book.ratings_count + 1 )
                    book.ratings_count += 1
                    book.save()

                return HttpResponse(json.dumps({'avg': "{:.1f}".format(book.average_rating), 'ratings_count':book.ratings_count, 'my': user_rating.rating}), status=200)

            # book does not exist
            else:
                return HttpResponse(_("Book does not exist"), status=404)

        # rating value is invalid
        else:
            return HttpResponse(_("Wrong rating value"), status=400)

    # this view can only be POST as ajax sends request
    else:
        return HttpResponse(_("Method not allowed"), status=405)


@login_required
def list_delete(request, username, list_slug):

    if request.user.username == username:
        list = List.objects.filter(slug=list_slug).first()

        if not list is None:

            if request.method == 'GET':
                list.delete()
                return redirect(reverse('booklists:lists_index', kwargs={'username': username}) + '?deleted=True')

            # this view can only be GET
            else:
                return render(request, 'booklists/errors/405.html', status=405)
        else:
            # not found
            return render(request, 'booklists/errors/404.html', status=404)
    else:
        # unauthorised
        return render(request, 'booklists/errors/401.html', status=401)


def search(request):
    search = request.GET.get('search')
    query_values = search.split()
    query = Q(name__contains=query_values[0])
    query_users = Q(username__contains=query_values[0])
    for value in query_values:
        query.add(Q(name__contains=value), Q.OR)
        query_users.add(Q(username__contains=value), Q.OR)

    books = Book.objects.filter(query)
    authors = Author.objects.filter(query)
    users = User.objects.filter(query_users)

    return render(request, 'booklists/search-results.html', context= {'books' : books, 'authors' : authors, 'users' : users, 'search' : search})

def author_show(request, author_slug):
    author = Author.objects.filter(slug=author_slug).first()

    if author:
        books = author.book_set.all()
        return render(request, 'booklists/authors/view.html', context={'author' : author, 'books' : books})
    else:
        # not found
        return render(request, 'booklists/errors/404.html', status=404)


@login_required
def book_add_to_list(request, username, list_slug, book_slug):

    book = Book.objects.filter(slug=book_slug).first()
    if not book is None:

        if request.method == 'GET':
            list = List.objects.filter(slug=list_slug).first()

            if not list is None:
                if list.user == request.user:
                    if not book in list.books.all():
                        list.books.add(book)
                else:
                    return render(request, 'booklists/errors/401.html', status=401)

            else:
                # not found
                return render(request, 'booklists/errors/404.html', status=404)

            return redirect(reverse('booklists:lists_view', kwargs={'username': request.user.username, 'list_slug': list.slug}) + '?added=True')

        # this view can only be GET
        else:
            return render(request, 'booklists/errors/405.html', status=405)
    else:
        # not found
        return render(request, 'booklists/errors/404.html', status=404)

@login_required
def book_delete_from_list(request, username, list_slug, book_slug):

    book = Book.objects.filter(slug=book_slug).first()

    if not book is None:

        if request.method == 'GET':
            list = List.objects.filter(slug=list_slug).first()

            if not list is None:
                if list.user == request.user:
                    if book in list.books.all():
                        list.books.remove(book)
                else:
                    return render(request, 'booklists/errors/401.html', status=401)
            else:
                # not found
                return render(request, 'booklists/errors/404.html', status=404)

            return redirect(reverse('booklists:lists_view', kwargs={'username': username, 'list_slug': list.slug}) + '?deleted=True')

        # this view can only be GET
        else:
            return render(request, 'booklists/errors/405.html', status=405)
    else:
        # not found
        return render(request, 'booklists/errors/404.html', status=404)


