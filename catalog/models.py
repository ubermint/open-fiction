from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from django.contrib.auth.models import User

class Book(models.Model):
    uid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=30)
    subject = ArrayField(models.CharField(max_length=25))
    year = models.PositiveIntegerField()
    word_count = models.PositiveIntegerField()
    description = models.TextField()
    ebook = models.BooleanField(default=False)
    price = models.FloatField(default=0)

    def subjects():
        return ("Memoir", "Nonfiction", "Fantasy", "Drama", "Horror",
        "Satire", "Children’s", "Adventure", "Philosophy", "Comedy", 
        "Shorts", "Poetry", "Spirituality", "Mystery", "Autobiography",
        "Science Fiction", "Fiction")

    def __str__(self):
    	return self.title

class Store(models.Model):
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30, default="")
    open_date = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100)
    coords = models.CharField(max_length=50, default="0, 0")
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.city

class Catalog(models.Model):
    count = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)    

class Employee(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)