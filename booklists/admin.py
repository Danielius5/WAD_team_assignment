from django.contrib import admin
from booklists.models import Book, Genre, Author, Rating, Comment, List

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(List)

