from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Textarea
from django.contrib.postgres.forms import SimpleArrayField

from .models import *


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class BookForm(forms.ModelForm):
    sub = Book.subjects()
    OPTIONS = list(zip(sub, sub))
    subject = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=OPTIONS)
    cover = forms.ImageField(required=False)
    ebook_file = forms.FileField(required=False)

    class Meta:
        model = Book
        fields = ("title", "author", "year", "subject", "word_count", "ebook", "description", "price")