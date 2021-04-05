import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_team_project.settings')


import django
django.setup()
from booklists.models import Book, Genre, Author, Rating, User, Comment, List


ADMIN_USERNAME = 'admin'
BOOK_USED = 'Blindside'
AUTHOR1 = 'James O. Born'
AUTHOR2 = 'James Patterson'
GENRE = 'Fiction'

def populate():
    genres = ['Sci-Fi','Horror','Action','Romance', 'Fiction']

    authors = ['Scott Fitzgerald','William Shakespeare','H.P. Lovecraft','William Blake', 'James O. Born', 'James Patterson']

    books = [
        {
            'name' : 'Blindside',
            'release_date' : '2020-06-21',
            'no_of_pages' : 352,
        },
    ]

    ratings = [
        {
            'user' : ADMIN_USERNAME,
            'book' : BOOK_USED,
            'rating' : 4,
        },
    ]

    comments = [
        {
            'user': ADMIN_USERNAME,
            'book': BOOK_USED,
            'comment': 'Amazing book! First comment as well, auto populated!',
        },
    ]

    lists = [
        {
            'user': ADMIN_USERNAME,
            'name': 'Great books',
        },
    ]

    for auth in authors:
        a=add_author(auth)

    for gen in genres:
        g=add_genre(gen)
    for book in books:
        add_book(book)
    for rating in ratings:
        add_rating(rating)
    for comment in comments:
        add_comment(comment)
    for list in lists:
        add_list(list)


        


def add_author(name):
    a=Author.objects.get_or_create(name=name)[0]
    print('added author: ' + a.name)
    return a

def add_genre(name):
    g=Genre.objects.get_or_create(name=name)[0]
    print('added genre: ' + g.name)
    return g

def add_book(dic):
    b = Book.objects.get_or_create(**dic)[0]
    print(b)
    print('added book: ' + b.name)
    b.authors.add(Author.objects.filter(name=AUTHOR1).first())
    b.authors.add(Author.objects.filter(name=AUTHOR2).first())
    print('assigned authors to the book')
    b.genre.add(Genre.objects.filter(name=GENRE).first())
    print('assigned genre to the book')

def add_rating(dic):
    dic['user'] = User.objects.filter(username=dic['user']).first()
    dic['book'] = Book.objects.filter(name=dic['book']).first()
    Rating.objects.get_or_create(**dic)
    print('added rating')

def add_comment(dic):
    dic['user'] = User.objects.filter(username=dic['user']).first()
    dic['book'] = Book.objects.filter(name=dic['book']).first()
    Comment.objects.get_or_create(**dic)
    print('added comment')

def add_list(dic):
    dic['user'] = User.objects.filter(username=dic['user']).first()
    list = List.objects.get_or_create(**dic)[0]
    print('added list')
    list.books.add(Book.objects.filter(name=BOOK_USED).first())
    print('assigned book to list')


if __name__=='__main__':
    print('starting population')
    if(not User.objects.filter(username='admin').exists()):
        print('\033[91m' + '\nPlease run $ python manage.py createsuperuser')
        print('\033[91m' + 'MAKE SURE the username is \'' + ADMIN_USERNAME + '\' for population script to work')

    else:
        populate()