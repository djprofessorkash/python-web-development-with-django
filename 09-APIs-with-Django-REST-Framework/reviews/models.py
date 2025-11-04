from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(upload_to="posters/", blank=True)
    release_date = models.DateField()

    def __str__(self):
        return self.title
    
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} by {self.reviewer.username}"
