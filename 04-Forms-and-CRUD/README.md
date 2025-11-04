# Day 4 — Library Project: Forms and CRUD

This tutorial walks through **Day 4** of our Django learning path: adding forms and CRUD functionality to our library project.

---

## Goals

- Create forms for Book, Author, and Genre models
- Implement Create, Read, Update, and Delete views
- Practice template usage for form rendering and submission
- Include validation and basic user feedback

---

## 1. Forms (`catalog/forms.py`)

```python
from django import forms
from .models import Book, Author, Genre

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'summary', 'isbn']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
```

---

## 2. Views (`catalog/views.py`)

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, Genre
from .forms import BookForm, AuthorForm, GenreForm

# Book CRUD

def book_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/book_list.html', {'books': books})


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'catalog/book_form.html', {'form': form})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/book_form.html', {'form': form})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'catalog/book_confirm_delete.html', {'book': book})
```

---

## 3. URLs (`catalog/urls.py`)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
]
```

Include `catalog.urls` in `pylibrary/urls.py`:

```python
path('', include('catalog.urls')),
```

---

## 4. Templates

### `book_list.html`
```django
{% extends 'base.html' %}
{% block content %}
<h2>Books</h2>
<a href="{% url 'book_create' %}">Add Book</a>
<ul>
    {% for book in books %}
        <li>
            {{ book.title }} by {{ book.author }}
            <a href="{% url 'book_update' book.pk %}">Edit</a>
            <a href="{% url 'book_delete' book.pk %}">Delete</a>
        </li>
    {% endfor %}
</ul>
{% endblock %}
```

### `book_form.html`
```django
{% extends 'base.html' %}
{% block content %}
<h2>{% if form.instance.pk %}Edit{% else %}Add{% endif %} Book</h2>
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
{% endblock %}
```

### `book_confirm_delete.html`
```django
{% extends 'base.html' %}
{% block content %}
<h2>Confirm Delete</h2>
<p>Are you sure you want to delete "{{ book.title }}"?</p>
<form method="post">{% csrf_token %}
    <button type="submit">Yes, delete</button>
    <a href="{% url 'book_list' %}">Cancel</a>
</form>
{% endblock %}
``` 

---

This completes **Day 4** of the **Python for Web Development** course and the second and final part of the library project, giving learners full CRUD functionality with forms and templates while preserving the modular workflow for future expansion.

---

### Recommended Stretch Challenges

1. **Form Validation**: Add custom validators for ISBN (e.g., length check, numeric).  
2. **Inline Author Creation**: Allow adding a new author directly from the Book creation form using `ModelChoiceField` with `empty_label` and JS enhancements.  
3. **Search Functionality**: Add a search box on the book list to filter by title or author.  
4. **Genre Assignment**: In the book form, display genres as checkboxes instead of the default multiple select.  
5. **Pagination**: Paginate book list to display 10 books per page using Django’s `Paginator` class. 