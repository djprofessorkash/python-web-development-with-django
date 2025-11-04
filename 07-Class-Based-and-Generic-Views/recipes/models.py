from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

DIFFICULTY_CHOICES = [
    ("E", "Easy"),
    ("M", "Medium"),
    ("H", "Hard")
]

class Chef(models.Model):
    """ 
    Model representing a recipe's author/chef.
    Chefs will be linked one-to-one with a Django user.
    """
    name = models.CharField(max_length=120)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Chef.objects.create(user=instance)

class Ingredient(models.Model):
    """ Model representing ingredient entity (e.g. egg, flour). """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Tag(models.Model):
    """ Model representing tags/labels for recipes (e.g. gluten-free, breakfast). """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """ Model representing a recipe, relating to its chef/author, composed ingredients, and related tags. """
    title = models.CharField(max_length=200)
    chef = models.ForeignKey(Chef, on_delete=models.SET_NULL, null=True, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes", blank=True)
    tags = models.ManyToManyField(Tag, related_name="recipes", blank=True)
    instructions = models.TextField()
    cook_time_in_minutes = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES, default="M")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at", "title"]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("recipe_detail", args=[str(self.id)])