# Day 3 — Library Project: Models, ORM, and Admin

This tutorial walks through **Day 3** of our Django learning path: building a simple library application using models, the Django ORM, and the admin interface. 

---

## Goals

- Define models for books, authors, and genres
- Create relationships using `ForeignKey` and `ManyToManyField`
- Register models in the admin for CRUD management
- Practice basic querying with the Django ORM

---

## 1. Project Setup

Create the project and virtual environment:

```bash
django-admin startproject pylibrary
cd pylibrary
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install django
```

Start the server to confirm setup:

```bash
python manage.py runserver
```

---

## 2. Create the `catalog` App

```bash
python manage.py startapp catalog
```

Add `catalog` to `INSTALLED_APPS` in `pylibrary/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'catalog',
]
```

---

## 3. Define Models (`catalog/models.py`)

```python
from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    summary = models.TextField(blank=True)
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
```

Run migrations:

```bash
python manage.py makemigrations catalog
python manage.py migrate
```

---

## 4. Register Models in Admin (`catalog/admin.py`)

```python
from django.contrib import admin
from .models import Author, Genre, Book

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
```

Access `/admin` to manage books, authors, and genres.

---

## 5. Basic ORM Queries (in Django shell)

```bash
python manage.py shell
```

```python
from catalog.models import Book, Author, Genre
Book.objects.all()
Book.objects.filter(title__icontains='Python')
Author.objects.get(id=1)
Genre.objects.filter(name='Science Fiction')
``` 

---

This completes **Day 3** of the **Python for Web Development** course and the first part of our library project.

---

### Recommended Stretch Challenges

1. **Book Cover Field**: Add an optional `ImageField` for book covers and display them in the admin.  
2. **Author Full Name Property**: Add a `full_name` property to `Author` and use it in admin list displays.  
3. **Custom Admin List Filters**: Filter books by genre and author in the admin using `list_filter`.  
4. **Query Practice**: Write ORM queries to find books with multiple genres or authors with more than 3 books. 