from django.test import TestCase
from booklists.models import *
from datetime import datetime,timedelta
from django.test import Client



#models test
class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.get_or_create(name='testauthor',about='This is a test case',)

    def test_author(self):
        guy=Author.objects.get(name="testauthor")
        self.assertEqual(guy.__str__(),"testauthor")
        self.assertEqual(guy.id,1)
        self.assertEqual(guy.slug,"1-testauthor")

class GenreTestCase(TestCase):
    def setUp(self):
        Genre.objects.get_or_create(name='testgenre')

    def test_genre(self):
        genre=Genre.objects.get(name="testgenre")
        self.assertEqual(genre.__str__(),"testgenre")
        self.assertEqual(genre.id,1)
        self.assertEqual(genre.slug,"1-testgenre")

class BookTestCase(TestCase):
    def setUp(self):

        current= datetime.today()
        Genre.objects.get_or_create(name='testgenre')
        Author.objects.get_or_create(name='testauthor')
        Author.objects.get_or_create(name='testauthor2')
        a=Book.objects.get_or_create(name='book',release_date=current,no_of_pages=4)
 


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
        User.objects.get_or_create(username='testuser',password='12345')
        Book.objects.get_or_create(name='book',release_date=current,no_of_pages=4, ratings_count=100)


        
        Comment.objects.get_or_create(user=User.objects.filter(id=1).first(),book=Book.objects.filter(id=1).first(),comment="This is the second test comment")
        Comment.objects.get_or_create(user=User.objects.filter(id=1).first(),book=Book.objects.filter(id=1).first(),comment="This is a test comment")

        
    def test_comment(self):
        
        c=Comment.objects.all().first()
        self.assertEqual(c.__str__(),"Comment This is a test comment by <bound method AbstractBaseUser.get_username of <User: testuser>>")
        self.assertEqual(c.id,2)#newest first



# Request tests
class HomeResponseTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_index(self):
        response = self.c.get('/booklists/', {})
        self.assertEqual(response.status_code, 200)

class LoginResponseTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.username = 'testuser25'
        self.password = '12345'
        self.user = User.objects.get_or_create(username=self.username, password=self.password)[0]
        self.user.set_password(self.password)
        self.user.save()

    def test_login_get(self):
        response = self.c.get('/booklists/login/', {})
        self.assertEqual(response.status_code, 200)

    def test_login_post_no_data(self):
        response = self.c.post('/booklists/login/', {})
        self.assertTemplateUsed(response, 'booklists/auth/login.html')

    def test_login_post_only_username(self):
        response = self.c.post('/booklists/login/', {'username' : self.username})
        self.assertTemplateUsed(response, 'booklists/auth/login.html')

    def test_login_post_only_password(self):
        response = self.c.post('/booklists/login/', {'password' : self.password})
        self.assertTemplateUsed(response, 'booklists/auth/login.html')

    def test_login_success(self):
        response = self.c.post('/booklists/login/', {'username' : self.username, 'password' : self.password})
        self.assertRedirects(response, '/booklists/')

        #check that logged in user cannot go to login

        response = self.c.get('/booklists/login/')
        self.assertRedirects(response, '/booklists/')

class RegisterResponseTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.username = 'testuser266'
        self.password = '12345abc.'

    def test_register_get(self):
        response = self.c.get('/booklists/register/', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booklists/auth/register.html')


    def test_register_post_no_data(self):
        response = self.c.post('/booklists/register/', {})
        self.assertTemplateUsed(response, 'booklists/auth/register.html')

    def test_register_post_only_username(self):
        response = self.c.post('/booklists/register/', {'username' : self.username})
        self.assertTemplateUsed(response, 'booklists/auth/register.html')

    def test_register_post_only_password_no_confirm(self):
        response = self.c.post('/booklists/register/', {'password1' : self.password})
        self.assertTemplateUsed(response, 'booklists/auth/register.html')

    def test_register_post_only_password_wrong_confirm(self):
        response = self.c.post('/booklists/register/', {'password1' : self.password, 'password2' : 'wrongPassword'})
        self.assertTemplateUsed(response, 'booklists/auth/register.html')

    def test_register_post_wrong_confirm(self):
        response = self.c.post('/booklists/register/', {'username' : self.username, 'password1' : self.password, 'password2' : 'wrongPassword'})
        self.assertTemplateUsed(response, 'booklists/auth/register.html')

    def test_register_easy_password(self):
        response = self.c.post('/booklists/register/', {'username' : self.username, 'password1' : '123', 'password2' : '123'})
        self.assertTemplateUsed(response, 'booklists/auth/register.html')

    def test_register_success(self):
        response = self.c.post('/booklists/register/', {'username' : self.username, 'password1' : self.password, 'password2' : self.password})

        # check that logged in user cannot go to login

        response = self.c.get('/booklists/register/')
        self.assertRedirects(response, '/booklists/')


class ListRequestTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.username = 'testuser25'
        self.password = '12345'
        self.user = User.objects.get_or_create(username=self.username, password=self.password)[0]
        self.user.set_password(self.password)
        self.user.save()

        self.c.login(username=self.username, password=self.password)
        self.list_private = List.objects.get_or_create(user=self.user, name='test_private', is_public=False)[0]



        self.username2 = 'testuseranother'
        self.user2 = User.objects.get_or_create(username=self.username2, password=self.password)[0]
        self.user2.set_password(self.password)
        self.user2.save()

        self.list_private_other_user = List.objects.get_or_create(user=self.user2, name='test_private', is_public=False)[0]

    def test_list_nonexisting_user(self):
        response = self.c.get('/booklists/user/nonexistinguser/lists', {})
        self.assertEqual(response.status_code, 404)

    def test_list_index(self):
        response = self.c.get('/booklists/user/' + self.username + '/lists', {})
        self.assertEqual(response.status_code, 200)

    def test_list_index_another_user(self):
        response = self.c.get('/booklists/user/' + self.username2 + '/lists', {})
        self.assertEqual(response.status_code, 200)

    def test_list_create_get_not_accessible_other_user(self):
        response = self.c.get('/booklists/user/' + self.username2 + '/lists/create', {})
        self.assertEqual(response.status_code, 401)

    def test_list_create_get(self):
        response = self.c.get('/booklists/user/' + self.username + '/lists/create', {})
        self.assertEqual(response.status_code, 200)

    def test_list_create_post_no_name(self):
        response = self.c.post('/booklists/user/' + self.username + '/lists/create', {})
        self.assertTemplateUsed(response, 'booklists/lists/create.html')

    def test_list_create_post_not_accessible_other_person(self):
        response = self.c.post('/booklists/user/' + self.username2 + '/lists/create', {'name' : 'tempTest'})
        self.assertEqual(response.status_code, 401)

    def test_list_create_post(self):
        response = self.c.post('/booklists/user/' + self.username + '/lists/create', {'name' : 'tempTest'})
        self.assertRedirects(response, '/booklists/user/' + self.username + '/lists?created=True')

    def test_list_cant_edit_other_user_list(self):
        response = self.c.get('/booklists/user/' + self.username2 + '/lists/' + self.list_private_other_user.slug + '/edit', {})
        self.assertEqual(response.status_code, 401)

    def test_list_edit_get(self):
        response = self.c.get('/booklists/user/' + self.username + '/lists/' + self.list_private.slug + '/edit', {})
        self.assertEqual(response.status_code, 200)

    def test_list_edit_post_no_name(self):
        response = self.c.post('/booklists/user/' + self.username + '/lists/' + self.list_private.slug + '/edit', {})
        self.assertTemplateUsed(response, 'booklists/lists/edit.html')

    def test_list_edit_post(self):
        response = self.c.post('/booklists/user/' + self.username + '/lists/' + self.list_private.slug + '/edit', {'name' : 'new_list_name'})
        self.assertRedirects(response, '/booklists/user/' + self.username + '/lists?edited=True')

        self.assertTrue(List.objects.filter(name='new_list_name').first())

    def test_list_delete_cant_other_user(self):
        response = self.c.get('/booklists/user/' + self.username2 + '/lists/' + self.list_private_other_user.slug + '/delete')
        self.assertEqual(response.status_code, 401)

    def test_list_delete(self):
        response = self.c.get('/booklists/user/' + self.username + '/lists/' + self.list_private.slug + '/delete')
        self.assertRedirects(response, '/booklists/user/' + self.username + '/lists?deleted=True')

        self.assertFalse(List.objects.filter(slug=self.list_private.slug).first())
