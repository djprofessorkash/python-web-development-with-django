from recipes.models import Recipe, Chef
from django.contrib.auth.models import User
from django.db.models import Count, Avg

# Recipes by a specific user.
user = User.objects.get(username="Kashy")
Recipe.objects.filter(chef__user=user)

# All users with greater-than-three (>3) recipes.
Chef.objects.annotate(num_recipes=Count("recipes")).filter(num_recipes__gt=3)

# All public stats. (Still available and unaffected by authentication.)
Recipe.objects.count()