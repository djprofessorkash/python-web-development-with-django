from django.db import models

# Create your models here.
class Genre(models.Model):
    """ Model representing a book's genre. (EX: fiction, sci-fi.) """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Author(models.Model):
    """ Model representing a book's author. """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_year = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["last_name", "first_name"]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Book(models.Model):
    """ Model representing a book's information with relationships to author and genre data. """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genre = models.ManyToManyField(Genre, related_name="books")
    publication_year = models.IntegerField()
    isbn = models.CharField("ISBN", max_length=13, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
