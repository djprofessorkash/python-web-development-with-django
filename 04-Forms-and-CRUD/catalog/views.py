from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book, Author, Publisher, Genre
from .forms import BookForm, AuthorForm, PublisherForm, GenreForm

####################################################################################################
########################################## VIEW: Homepage ##########################################
####################################################################################################

# READ: Homepage. 
def home(request):
    context = {
        "page_title": "Welcome to the PyLibrary!",
        "intro": "Check out our vast selection of books and written works!"
    }
    return render(request, "catalog/home.html", context)

####################################################################################################
########################################### VIEWS: Books ###########################################
####################################################################################################

# READ: All Books. Leverages Optional Search Query Filter.
def book_list(request):
    """ Displays list of all books with optional search filtering. """
    query = request.GET.get("q")
    books = Book.objects.select_related("author", "publisher").prefetch_related("genre").all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) | 
            Q(author__last_name__icontains=query)
        )

    return render(request, "catalog/book/book_list.html", {"books": books})

# CREATE: Add New Book.
def add_book(request):
    """ Create new book using input form. """
    default_publisher = Publisher.objects.filter(name="Open Learning Press").first()
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            messages.success(request, f'"{new_book.title}" has been added to the catalog!')
            return redirect("book_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm(initial={"publisher": default_publisher})
    return render(request, "catalog/book/add_book.html", {"form": form})

# READ: View Individual Book by ID.
def book_detail(request, book_id):
    """ Displays detailed information about one book. """
    book = get_object_or_404(Book.objects.select_related("author", "publisher").prefetch_related("genre"), pk=book_id)
    return render(request, "catalog/book/book_detail.html", {"book": book})

# UPDATE: Edit Existing Book by ID.
def edit_book(request, book_id):
    """ Edit an existing book. """
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{book.title}" has been updated.')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, "catalog/book/edit_book.html", {"form": form, "book": book})

# DELETE: Remove Existing Book by ID.
def delete_book(request, book_id):
    """ Delete an existing book (with confirmation). """
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        messages.success(request, f'"{book.title}" has been deleted from the catalog.')
        return redirect("book_list")
    return render(request, "catalog/book/delete_book.html", {"book": book})

####################################################################################################
########################################## VIEWS: Authors ##########################################
####################################################################################################

# READ: All Authors. 
def author_list(request):
    """ Displays list of all authors. """
    authors = Author.objects.all()
    return render(request, "catalog/author/author_list.html", {"authors": authors})

# CREATE: Add New Author.
def add_author(request):
    """ Create new author using input form. """
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()
            messages.success(request, f'Author "{new_author}" created successfully!')
            return redirect("book_list")
    else:
        form = AuthorForm()
    return render(request, "catalog/author/add_author.html", {"form": form})

# READ: View Individual Author by ID.
def author_detail(request, author_id):
    """ Show details and books for a single author. """
    author = get_object_or_404(Author, pk=author_id)
    books = Book.objects.filter(author=author).select_related("publisher")
    return render(request, "catalog/author/author_detail.html", {
        "author": author,
        "books": books
    })

# UPDATE: Edit Existing Author by ID.
def edit_author(request, author_id):
    """ Edit an existing author. """
    author = get_object_or_404(Author, pk=author_id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{author.first_name} {author.last_name}" has been updated.')
            return redirect('author_detail', author_id=author.id)
    else:
        form = AuthorForm(instance=author)
    return render(request, "catalog/author/edit_author.html", {"form": form, "author": author})

# DELETE: Remove Existing Author by ID.
def delete_author(request, author_id):
    """ Delete an existing author (with confirmation). """
    author = get_object_or_404(Author, pk=author_id)
    if request.method == "POST":
        author.delete()
        messages.success(request, f'"{author.first_name} {author.last_name}" has been deleted from the catalog.')
        return redirect("author_list")
    return render(request, "catalog/author/delete_author.html", {"author": author})

####################################################################################################
######################################## VIEWS: Publishers #########################################
####################################################################################################

# READ: All Publishers. 
def publisher_list(request):
    """ Displays list of all publishers. """
    publishers = Publisher.objects.all()
    return render(request, "catalog/publisher/publisher_list.html", {"publishers": publishers})

# CREATE: Add New Publisher.
def add_publisher(request):
    """ Create new publisher using input form. """
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            new_publisher = form.save()
            messages.success(request, f'Publisher "{new_publisher}" created successfully!')
            return redirect("book_list")
    else:
        form = PublisherForm()
    return render(request, "catalog/publisher/add_publisher.html", {"form": form})

# READ: View Individual Publisher by ID.
def publisher_detail(request, publisher_id):
    """ Show details and books for a single publisher. """
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    books = Book.objects.filter(publisher=publisher).select_related("author")
    return render(request, "catalog/publisher/publisher_detail.html", {
        "publisher": publisher,
        "books": books
    })

# UPDATE: Edit Existing Publisher by ID.
def edit_publisher(request, publisher_id):
    """ Edit an existing publisher. """
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{publisher.name}" has been updated.')
            return redirect('publisher_detail', publisher_id=publisher.id)
    else:
        form = PublisherForm(instance=publisher)
    return render(request, "catalog/publisher/edit_publisher.html", {"form": form, "publisher": publisher})

# DELETE: Remove Existing Publisher by ID.
def delete_publisher(request, publisher_id):
    """ Delete an existing publisher (with confirmation). """
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    if request.method == "POST":
        publisher.delete()
        messages.success(request, f'"{publisher.name}" has been deleted from the catalog.')
        return redirect("publisher_list")
    return render(request, "catalog/publisher/delete_publisher.html", {"publisher": publisher})

####################################################################################################
########################################## VIEWS: Genres ###########################################
####################################################################################################

# READ: All Genres. 
def genre_list(request):
    """ Displays list of all genres. """
    genres = Genre.objects.all()
    return render(request, "catalog/genre/genre_list.html", {"genres": genres})

# CREATE: Add New Genre.
def add_genre(request):
    """ Create new genre using input form. """
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            new_genre = form.save()
            messages.success(request, f'Publisher "{new_genre}" created successfully!')
            return redirect("book_list")
    else:
        form = GenreForm()
    return render(request, "catalog/genre/add_genre.html", {"form": form})

# READ: View Individual Genre by ID.
def genre_detail(request, genre_id):
    """ Show books belonging to a specific genre. """
    genre = get_object_or_404(Genre, pk=genre_id)
    books = genre.books.select_related("author", "publisher").all()
    return render(request, "catalog/genre/genre_detail.html", {
        "genre": genre,
        "books": books
    })

# UPDATE: Edit Existing Genre by ID.
def edit_genre(request, genre_id):
    """ Edit an existing genre. """
    genre = get_object_or_404(Genre, pk=genre_id)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{genre.name}" has been updated.')
            return redirect('genre_detail', genre_id=genre.id)
    else:
        form = GenreForm(instance=genre)
    return render(request, "catalog/genre/edit_genre.html", {"form": form, "genre": genre})

# DELETE: Remove Existing Genre by ID.
def delete_genre(request, genre_id):
    """ Delete an existing genre (with confirmation). """
    genre = get_object_or_404(Genre, pk=genre_id)
    if request.method == "POST":
        genre.delete()
        messages.success(request, f'"{genre.name}" has been deleted from the catalog.')
        return redirect("genre_list")
    return render(request, "catalog/genre/delete_genre.html", {"genre": genre})
