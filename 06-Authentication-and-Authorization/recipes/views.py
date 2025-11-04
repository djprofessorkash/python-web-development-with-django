from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Recipe, Chef, Ingredient, Tag
from .forms import RecipeForm, SignUpForm

# USER REGISTRATION.
def signup_view(request):
    """ Enable new users to register account. """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("recipe_list")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

# READ: Display All Recipes.
def recipe_list(request):
    qs = Recipe.objects.select_related("chef").prefetch_related("ingredients", "tags").all()

    # Simple filters via GET params.
    tag = request.GET.get("tag")
    ingredient = request.GET.get("ingredient")
    chef = request.GET.get("chef")
    q = request.GET.get("q")

    if tag:
        qs = qs.filter(tags__name__iexact=tag)
    if ingredient:
        qs = qs.filter(ingredients__name__iexact=ingredient)
    if chef:
        qs = qs.filter(chef__name__icontains=chef)
    if q:
        qs = qs.filter(title__icontains=q)

    # Distinct because of JOINs.
    qs = qs.distinct()

    # Basic pagination.
    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "recipes/recipe_list.html", {"page_obj": page_obj})

# READ: Display Individual Recipe by ID.
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.select_related("chef").prefetch_related("ingredients", "tags"), pk=pk)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})

# CREATE: Add New Recipe. (Requires user authorization.)
@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.chef = Chef.objects.get(user=request.user)
            new_recipe.save()
            form.save_m2m()
            return redirect(new_recipe.get_absolute_url())
    else:
        form = RecipeForm()
    return render(request, "recipes/recipe_form.html", {"form": form, "action": "Create"})

# READ: Display User's Recipes. (Requires user authorization.)
@login_required
def my_recipes(request):
    chef = Chef.objects.get(user=request.user)
    my_recipes = Recipe.objects.filter(chef=chef).select_related("chef")
    return render(request, "recipes/my_recipes.html", {"recipes": my_recipes})

# UPDATE: Edit Existing Recipe by ID. (Requires user authorization.)
@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.chef.user != request.user:
        return HttpResponseForbidden("You do not have permission to edit this recipe.")
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect(recipe.get_absolute_url())
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipes/recipe_form.html", {"form": form, "action": "Edit"})

# DELETE: Delete Existing Recipe by ID. (Requires user authorization.)
@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.chef.user != request.user:
        return HttpResponseForbidden("You cannot delete another user's recipe.")
    if request.method == "POST":
        recipe.delete()
        return redirect("recipe_list")
    return render(request, "recipes/recipe_confirm_delete.html", {"recipe": recipe})

# Aggregations / Advanced examples for dashboards
def stats_dashboard(request):
    # Number of recipes per chef (annotate)
    chefs_counts = Chef.objects.annotate(recipe_count=Count("recipes")).order_by("-recipe_count")

    # Average cook time across all recipes
    avg_cook_time = Recipe.objects.aggregate(avg_time=Avg("cook_time_in_minutes"))["avg_time"]

    # Top 5 recipes with most ingredients
    top_recipes_by_ingredients = Recipe.objects.annotate(num_ingredients=Count("ingredients")).order_by("-num_ingredients")[:5]

    return render(request, "recipes/stats.html", {
        "chefs_counts": chefs_counts,
        "avg_cook_time": avg_cook_time,
        "top_recipes_by_ingredients": top_recipes_by_ingredients,
    })