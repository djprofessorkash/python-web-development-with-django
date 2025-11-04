from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipes/add/", views.recipe_create, name="recipe_create"),
    path("recipes/<int:pk>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipes/<int:pk>/delete/", views.recipe_delete, name="recipe_delete"),
    path("my-recipes/", views.my_recipes, name="my_recipes"),
    path("stats/", views.stats_dashboard, name="recipes_stats"),
    path("signup/", views.signup_view, name="signup"),
]