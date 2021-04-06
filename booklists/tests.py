from django.test import TestCase
from booklists.models import *
from datetime import datetime,timedelta
# Create your tests here.


#models test
class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(name='testauthor',about='This is a test case',)

    def test_author(self):
        guy=Author.objects.get(name="testauthor")
        self.assertEqual(guy.__str__(),"testauthor")
        self.assertEqual(guy.id,1)
        self.assertEqual(guy.slug,"1-testauthor")

class GenreTestCase(TestCase):
    def setUp(self):
        Genre.objects.create(name='testgenre')

    def test_genre(self):
        genre=Genre.objects.get(name="testgenre")
        self.assertEqual(genre.__str__(),"testgenre")
        self.assertEqual(genre.id,1)
        self.assertEqual(genre.slug,"1-testgenre")

class BookTestCase(TestCase):
    def setUp(self):

        current= datetime.today()
        Genre.objects.create(name='testgenre')
        Author.objects.create(name='testauthor')
        Author.objects.create(name='testauthor2')
        a=Book.objects.create(name='book',release_date=current,no_of_pages=4)
 


    def test_book(self):


        book=Book.objects.get(name="book")
        self.assertEqual(book.__str__(),"book")
        self.assertEqual(book.id,1)
        self.assertEqual(book.slug,"1-book")
        
        self.assertEqual(book.average_rating,0.0) #default
        self.assertEqual(book.ratings_count,0)

        book.authors.add(Author.objects.filter(name='testauthor').first())
        book.authors.add(Author.objects.filter(name='testauthor2').first())

        
        book.genre.add(Genre.objects.filter(name='testgenre').first())
        book.genre.add(Genre.objects.filter(name='testgenre').first())

class RatingTestCase(TestCase):
    def setUp(self):
        return

    def test_rating(self):
        return
        
        
class CommentTestCase(TestCase):
    def setUp(self):
        current= datetime.today()
        User.objects.create(username='testuser',password='12345')
        Book.objects.create(name='book',release_date=current,no_of_pages=4, ratings_count=100)


        
        Comment.objects.create(user=User.objects.filter(id=1).first(),book=Book.objects.filter(id=1).first(),comment="This is the second test comment")
        Comment.objects.create(user=User.objects.filter(id=1).first(),book=Book.objects.filter(id=1).first(),comment="This is a test comment")

        
    def test_comment(self):
        
        c=Comment.objects.all().first()
        self.assertEqual(c.__str__(),"Comment This is a test comment by <bound method AbstractBaseUser.get_username of <User: testuser>>")
        self.assertEqual(c.id,2)#newest first



#Views test
