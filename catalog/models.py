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

    def __str__(self):
    	return self.title

"""
    class Genres(models.TextChoices):
        JAN = "January"
        FEB = "February"
        MAR = "March"
        DEC = "December"

    genre = ArrayField(models.TextField(choices=Genres, max_length=2, blank=True))
"""
    

class Store(models.Model):
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.city

class Catalog(models.Model):
    count = models.PositiveIntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)