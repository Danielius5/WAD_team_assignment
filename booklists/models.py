from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
  
    
class Author(models.Model):
    
    name = models.CharField(max_length=128)
    about = models.TextField(max_length=256,null=True,blank=True)
        
    def __str__(self):
        return self.name
    
class Genre(models.Model):
    
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):

    authors = models.ManyToManyField(Author)
    name = models.CharField(max_length=128)
    release_date = models.DateField()
    no_of_pages = models.IntegerField()
    cover = models.ImageField(upload_to='book_covers',default='/images/picturenotfound.jpg')
    genre = models.ManyToManyField(Genre)
    
    def __str__(self):
        return self.name
    
class Rating(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(
            validators=[MaxValueValidator(5), MinValueValidator(1)]
        )
    
    def __str__(self):
        return "id: " + self.id + " rating: " + self.rating
    
class Comment(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user.get_username)
    
class List(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    name = models.CharField(max_length=128)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name