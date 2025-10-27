from django.urls import path
from . import views

urlpatterns = [
    # Homepage.
    path("", views.home, name="home"),

    # CRUD: Books.
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.add_book, name="add_book"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("books/<int:book_id>/edit/", views.edit_book, name="edit_book"),
    path("books/<int:book_id>/delete/", views.delete_book, name="delete_book"),

    # CRUD: Authors.
    path("authors/", views.author_list, name="author_list"),
    path("authors/add/", views.add_author, name="add_author"),
    path("authors/<int:author_id>/", views.author_detail, name="author_detail"),
    path("authors/<int:author_id>/edit/", views.edit_author, name="edit_author"),
    path("authors/<int:author_id>/delete/", views.delete_author, name="delete_author"),

    # CRUD: Publishers.
    path("publishers/", views.publisher_list, name="publisher_list"),
    path("publishers/add/", views.add_publisher, name="add_publisher"),
    path("publishers/<int:publisher_id>/", views.publisher_detail, name="publisher_detail"),
    path("publishers/<int:publisher_id>/edit/", views.edit_publisher, name="edit_publisher"),
    path("publishers/<int:publisher_id>/delete", views.delete_publisher, name="delete_publisher"),

    # CRUD: Genres.
    path("genres/", views.genre_list, name="genre_list"),
    path("genres/add/", views.add_genre, name="add_genre"),
    path("genres/<int:genre_id>/", views.genre_detail, name="genre_detail"),
    path("genres/<int:genre_id>/edit/", views.edit_genre, name="edit_genre"),
    path("genres/<int:genre_id>/delete", views.delete_genre, name="delete_genre"),
]