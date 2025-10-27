from django import forms
from django.core.validators import RegexValidator
from .models import Book, Author, Publisher, Genre

isbn_validator = RegexValidator(r'%\d{13}$', 'Enter a valid 13-digit ISBN.')

class BookForm(forms.ModelForm):
    """ Input form for creating and editing <Book> entries. """
    isbn = forms.CharField(validators=[isbn_validator])
    class Meta:
        model = Book
        fields = ["title", "author", "publisher", "genre", "publication_year", "isbn"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Book Title"}),
            "publisher_year": forms.NumberInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 9781234567890"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "publisher": forms.Select(attrs={"class": "form-control"}),
            "genre": forms.CheckboxSelectMultiple(),
        }

class AuthorForm(forms.ModelForm):
    """ Input form for creating and editing <Author> entries. """
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "birth_year"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "birth_year": forms.NumberInput(attrs={"class": "form-control"}),
        }

class PublisherForm(forms.ModelForm):
    """ Input form for creating and editing <Publisher> entries. """
    class Meta:
        model = Publisher
        fields = ["name", "city", "country"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }

class GenreForm(forms.ModelForm):
    """ Input form for creating and editing <Genre> entries. """
    class Meta:
        model = Genre
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }