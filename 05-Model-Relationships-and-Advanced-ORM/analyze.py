from recipes.models import Recipe, Chef, Ingredient, Tag
from django.db.models import Count, Avg

# Retrieve list with related data.
recipes = Recipe.objects.select_related("chef").prefetch_related("ingredients", "tags").all()
for recipe in recipes[:5]:
    print(recipe.title, 
          recipe.chef and recipe.chef.name, 
          [ingredient.name for ingredient in recipe.ingredients.all()])
    
# Count recipes per chef using `.annotate()`.
Chef.objects.annotate(recipe_count=Count("recipes")).order_by("-recipe_count")

# Get top five recipes with most ingredients using `.annotate()`.
Recipe.objects.annotate(num_ingredients=Count("ingredients")).order_by("-num_ingredients")[:5]

# Get average cooking time in minutes using `.aggregate()`.
Recipe.objects.aggregate(avg_time=Avg("cook_time_in_minutes"))

# Get recipes that include "egg" as an ingredient using `.filter()`.
Recipe.objects.filter(ingredients__name__iexact="egg").distinct()

# Get breakfast/brunch recipes sorted by ingredient quantity using method chaining with `.filter(...).annotate(...)`.
Recipe.objects.filter(tags__name__in=["breakfast", "brunch"]).annotate(num_ingredients=Count("ingredients")).order_by("-num_ingredients")

# Get all ingredients used by the first chef's recipes
chef = Chef.objects.first()
Ingredient.objects.filter(recipes__chef=chef).distinct()