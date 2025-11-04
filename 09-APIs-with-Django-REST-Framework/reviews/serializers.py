from rest_framework import serializers
from .models import Movie, Review, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ["id", "movie", "reviewer", "rating", "comment", "created_at"]
    
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "genres", "poster", "release_date", "reviews"]