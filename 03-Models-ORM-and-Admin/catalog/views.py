from django.shortcuts import render
from .models import Book

# Create your views here.
def home(request):
    context = {
        'page_title': 'Welcome to the PyLibrary!',
        'intro': 'Check out our vast selection of books and written works!'
    }
    return render(request, 'catalog/home.html', context)

def book_list(request):
    books = Book.objects.select_related('author').prefetch_related('genre').all()
    return render(request, 'catalog/book_list.html', {'books': books})
