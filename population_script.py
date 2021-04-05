import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_team_project.settings')


import django
django.setup()
from booklists.models import Book, Genre, Author, Rating, User, Comment, List

def populate():
    genres = ['Sci-Fi','Horror','Action','Romance']

    authors = ['Scott Fitzgerald','William Shakespeare','H.P. Lovecraft','William Blake']


    for auth in authors:
        a=add_author(auth)

    for gen in genres:
        g=add_genre(gen)    


        


def add_author(name):
    a=Author.objects.get_or_create(name=name)[0]
    a.save
    return a




def add_book():
    return



def add_genre(name):
    g=Genre.objects.get_or_create(name=name)[0]
    g.save()
    return g




if __name__=='__main__':
    print('starting population')
    populate()