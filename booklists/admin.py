from django.contrib import admin
from booklists.models import Book,Author,Genre
from booklists.models import UserProfile

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)

